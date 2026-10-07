import subprocess
import sys
import os
import time
import ast
import tempfile
from pathlib import Path
from django.conf import settings

# Disallowed modules and builtins for security
DISALLOWED_MODULES = {
    'subprocess', 'multiprocessing', 'pty', 'posix', 'nt',
    'socket', 'urllib', 'http', 'ftplib', 'smtplib', 'imaplib', 'poplib',
    'ctypes', 'winreg', 'msvcrt', '_winapi', 'shutil', 'asyncio'
}

DISALLOWED_CALLS = {
    ('os', 'system'), ('os', 'popen'), ('os', 'spawn'), ('os', 'execl'),
    ('os', 'execle'), ('os', 'execlp'), ('os', 'execlpe'), ('os', 'execv'),
    ('os', 'execve'), ('os', 'execvp'), ('os', 'execvpe'), ('os', 'remove'),
    ('os', 'unlink'), ('os', 'rmdir'), ('os', 'removedirs'), ('os', 'rename'),
    ('os', 'renames'), ('os', 'replace'), ('os', 'kill'), ('os', 'killpg'),
}

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        for alias in node.names:
            base_mod = alias.name.split('.')[0]
            if base_mod in DISALLOWED_MODULES:
                self.errors.append(f"Security restriction: module '{alias.name}' is not allowed in sandbox.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_mod = node.module.split('.')[0]
            if base_mod in DISALLOWED_MODULES:
                self.errors.append(f"Security restriction: module '{node.module}' is not allowed in sandbox.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            pair = (node.value.id, node.attr)
            if pair in DISALLOWED_CALLS:
                self.errors.append(f"Security restriction: '{node.value.id}.{node.attr}' is not permitted.")
        self.generic_visit(node)


def sanitize_code(code_string):
    """
    Parses code AST to check for forbidden calls or syntax errors prior to execution.
    """
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"

    visitor = SecurityVisitor()
    visitor.visit(tree)
    if visitor.errors:
        return False, " | ".join(visitor.errors)

    return True, None


def execute_python_code(code_string, stdin_input="", timeout=None):
    """
    Executes Python code inside an isolated subprocess worker with strict timeouts,
    clean environment, memory guards, and execution isolation.
    """
    if timeout is None:
        timeout = getattr(settings, 'SANDBOX_TIMEOUT_SECONDS', 4)
    max_bytes = getattr(settings, 'SANDBOX_MAX_OUTPUT_BYTES', 65536)

    # 1. AST Static security check
    is_safe, error_msg = sanitize_code(code_string)
    if not is_safe:
        return {
            'status': 'error',
            'stdout': '',
            'stderr': error_msg,
            'execution_time': 0.0,
            'exit_code': 1,
            'is_timeout': False
        }

    # 2. Prepare isolated temporary scratch folder
    with tempfile.TemporaryDirectory(prefix="py_sandbox_") as scratch_dir:
        script_path = Path(scratch_dir) / "user_script.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code_string)

        # 3. Form isolated subprocess environment
        # Strip all sensitive server environment variables
        isolated_env = {
            'PYTHONSAFEPATH': '1',
            'PYTHONIOENCODING': 'utf-8',
            'PYTHONDONTWRITEBYTECODE': '1',
            'PATH': os.environ.get('PATH', ''),
            'SYSTEMROOT': os.environ.get('SYSTEMROOT', r'C:\Windows'),
            'TEMP': scratch_dir,
            'TMP': scratch_dir,
        }

        # Use current Python interpreter with -I (Isolated mode)
        cmd = [sys.executable, "-I", str(script_path)]

        start_time = time.time()
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=scratch_dir,
                env=isolated_env,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            stdout_data, stderr_data = process.communicate(
                input=stdin_input or None,
                timeout=timeout
            )
            elapsed_time = round(time.time() - start_time, 3)

            # Cap outputs to avoid memory exhaustion
            if len(stdout_data.encode('utf-8')) > max_bytes:
                stdout_data = stdout_data[:max_bytes] + "\n...[Output truncated due to size limit]"
            if len(stderr_data.encode('utf-8')) > max_bytes:
                stderr_data = stderr_data[:max_bytes] + "\n...[Error output truncated]"

            status = 'success' if process.returncode == 0 else 'error'

            return {
                'status': status,
                'stdout': stdout_data,
                'stderr': stderr_data,
                'execution_time': elapsed_time,
                'exit_code': process.returncode,
                'is_timeout': False
            }

        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.communicate(timeout=1)
            except Exception:
                pass
            elapsed_time = round(time.time() - start_time, 3)
            return {
                'status': 'timeout',
                'stdout': '',
                'stderr': f"Execution timed out after {timeout} seconds. Infinite loop detected or long-running operation.",
                'execution_time': elapsed_time,
                'exit_code': -1,
                'is_timeout': True
            }
        except Exception as e:
            elapsed_time = round(time.time() - start_time, 3)
            return {
                'status': 'error',
                'stdout': '',
                'stderr': f"Runtime execution failure: {str(e)}",
                'execution_time': elapsed_time,
                'exit_code': -1,
                'is_timeout': False
            }
