"""
Seed data definitions for real-world Python projects across Beginner, Intermediate, and Advanced tiers.
"""

from projects.models import Project

def seed_projects():
    print("Seeding Real Python Projects...")

    projects_data = [
        # --- BEGINNER ---
        {
            'title': 'Command-Line Calculator',
            'slug': 'command-line-calculator',
            'level': 'beginner',
            'order': 1,
            'description': 'A clean, menu-driven CLI calculator supporting arithmetic operations, error handling for division by zero, and operation history.',
            'requirements': 'Python 3.8+\nBasic understanding of functions, loops, and conditional statements\nNo external third-party dependencies required',
            'concepts_used': 'Functions, While Loops, Match-Case/If-Elif, Exception Handling, Data Types',
            'step_by_step_guide': '''### Step 1: Define Arithmetic Functions
Create pure functions for addition, subtraction, multiplication, and division. Ensure division checks for zero.

### Step 2: Implement Calculation Loop
Use a `while True:` loop to display a clean menu and prompt the user for choice and numbers.

### Step 3: Handle Invalid Input
Wrap number conversion in `try...except ValueError` blocks to guard against invalid non-numeric inputs.

### Step 4: Track Operation History
Store past calculations in a list of formatted strings and provide a menu option to review past results.''',
            'source_code': '''def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0: raise ValueError("Cannot divide by zero.")
    return a / b

history = []

def run_calculator():
    print("=== PyMaster CLI Calculator ===")
    operations = {"1": ("+", add), "2": ("-", subtract), "3": ("*", multiply), "4": ("/", divide)}
    
    while True:
        print("\\n1. Add | 2. Subtract | 3. Multiply | 4. Divide | 5. View History | 6. Exit")
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "6":
            print("Thanks for using the calculator. Goodbye!")
            break
        elif choice == "5":
            print("\\n--- Calculation History ---")
            for record in history or ["No calculations performed yet."]:
                print(record)
            continue
            
        if choice in operations:
            symbol, func = operations[choice]
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = func(num1, num2)
                record = f"{num1} {symbol} {num2} = {result}"
                history.append(record)
                print("Result:", result)
            except ValueError as e:
                print("Error:", e)
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    run_calculator()''',
            'challenges': '* Add square root and power operations using the math module.\n* Add functionality to export the session calculation history to a text file.'
        },
        {
            'title': 'Number Guessing Game',
            'slug': 'number-guessing-game',
            'level': 'beginner',
            'order': 2,
            'description': 'An interactive terminal game where the computer picks a random secret number, and the player guesses with dynamic feedback and score rating.',
            'requirements': 'Python 3.8+\nStandard library random module\nConsole input/output',
            'concepts_used': 'Random module, Loops, Input validation, Comparison operators, Scoring logic',
            'step_by_step_guide': '''### Step 1: Generate the Random Number
Use `random.randint(1, 100)` to pick the secret number.

### Step 2: Set Difficulty Levels
Allow the user to select Easy (10 attempts), Medium (7 attempts), or Hard (5 attempts).

### Step 3: Implement Guess Evaluation
Compare the guess with the target and output "Too high!" or "Too low!".

### Step 4: Display Win/Loss Report
Calculate score percentage based on attempts remaining.''',
            'source_code': '''import random

def play_game():
    print("=== Number Guessing Challenge ===")
    secret = random.randint(1, 100)
    attempts_allowed = 7
    attempts_taken = 0
    
    print("I have chosen a secret number between 1 and 100. Can you guess it in 7 tries?")
    
    while attempts_taken < attempts_allowed:
        try:
            guess = int(input(f"\\nAttempt {attempts_taken + 1}/{attempts_allowed} - Enter your guess: "))
        except ValueError:
            print("Please enter a valid integer.")
            continue
            
        attempts_taken += 1
        
        if guess == secret:
            score = (attempts_allowed - attempts_taken + 1) * 15
            print(f"🎉 Bullseye! You guessed {secret} in {attempts_taken} attempts! Score: {score} pts")
            return
        elif guess < secret:
            print("Too low! ⬆️ Try a higher number.")
        else:
            print("Too high! ⬇️ Try a lower number.")
            
    print(f"\\nGame Over! The secret number was {secret}. Better luck next time!")

if __name__ == "__main__":
    play_game()''',
            'challenges': '* Allow two players to compete against each other in turns.\n* Provide "Hot" / "Cold" hints based on distance from the secret number.'
        },
        {
            'title': 'Terminal To-Do List Application',
            'slug': 'terminal-todo-list',
            'level': 'beginner',
            'order': 3,
            'description': 'A clean task organizer allowing users to add, list, complete, and delete tasks with persistent JSON storage.',
            'requirements': 'Python 3.8+\njson standard library module',
            'concepts_used': 'Lists, Dictionaries, File I/O, JSON serialization, Defensive programming',
            'step_by_step_guide': '''### Step 1: Model Tasks
Model each task as a dictionary with `id`, `title`, and `completed` boolean status.

### Step 2: Implement File Persistence
Read and write tasks to a `todos.json` file using the `json` module.

### Step 3: Provide CRUD Operations
Build functions: `add_task(title)`, `list_tasks()`, `complete_task(id)`, and `delete_task(id)`.

### Step 4: Create Command Loop
Wire user interactions into an interactive menu with status indicators [✓] and [ ].''',
            'source_code': '''import json
import os

DB_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def list_tasks(tasks):
    print("\\n=== Your Task List ===")
    if not tasks:
        print("No tasks found. Your list is empty!")
        return
    for t in tasks:
        status = "✓" if t["completed"] else " "
        print(f"[{status}] #{t['id']}: {t['title']}")

def add_task(tasks, title):
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "title": title, "completed": False})
    save_tasks(tasks)
    print(f"Task #{new_id} added successfully.")

def complete_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            save_tasks(tasks)
            print(f"Task #{task_id} marked as completed!")
            return
    print("Task ID not found.")

def main():
    tasks = load_tasks()
    while True:
        print("\\n1. List Tasks | 2. Add Task | 3. Complete Task | 4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            title = input("Enter task title: ").strip()
            if title: add_task(tasks, title)
        elif choice == "3":
            try:
                tid = int(input("Enter task ID to complete: "))
                complete_task(tasks, tid)
            except ValueError:
                print("Invalid ID.")
        elif choice == "4":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()''',
            'challenges': '* Add priority levels (Low, Medium, High) with colored terminal badges.\n* Add due date sorting and task search.'
        },

        # --- INTERMEDIATE ---
        {
            'title': 'Personal Expense Tracker',
            'slug': 'personal-expense-tracker',
            'level': 'intermediate',
            'order': 4,
            'description': 'A financial management system allowing categorization of expenses, budget caps, and analytical category spending breakdown.',
            'requirements': 'Python 3.9+\nCSV or JSON file handling\nObject-Oriented Design',
            'concepts_used': 'OOP Classes, Datetime manipulation, File I/O, Data Aggregation, Lambda sorting',
            'step_by_step_guide': '''### Step 1: Define Expense Class
Create an `Expense` class storing amount, category, description, and timestamp.

### Step 2: Implement ExpenseTracker Manager
Build the manager with methods to add expense, filter by date range, and calculate category totals.

### Step 3: Generate Summary Reports
Compute total spending, compare against budget, and calculate percentage per category.''',
            'source_code': '''from datetime import datetime
from collections import defaultdict

class Expense:
    def __init__(self, amount: float, category: str, description: str):
        self.amount = float(amount)
        self.category = category.title()
        self.description = description
        self.date = datetime.now()

class ExpenseTracker:
    def __init__(self, monthly_budget: float = 1000.0):
        self.expenses = []
        self.monthly_budget = monthly_budget

    def add_expense(self, amount: float, category: str, description: str):
        exp = Expense(amount, category, description)
        self.expenses.append(exp)
        return exp

    def total_spending(self):
        return sum(e.amount for e in self.expenses)

    def category_breakdown(self):
        breakdown = defaultdict(float)
        for e in self.expenses:
            breakdown[e.category] += e.amount
        return dict(breakdown)

    def generate_report(self):
        total = self.total_spending()
        remaining = self.monthly_budget - total
        print("=== Expense Summary Report ===")
        print(f"Total Spent: ${total:.2f} / Budget: ${self.monthly_budget:.2f}")
        print(f"Remaining Budget: ${remaining:.2f}\\n")
        print("Category Spending:")
        for cat, spent in sorted(self.category_breakdown().items(), key=lambda x: x[1], reverse=True):
            pct = (spent / total * 100) if total > 0 else 0
            print(f"  • {cat:15}: ${spent:.2f} ({pct:.1f}%)")

if __name__ == "__main__":
    tracker = ExpenseTracker(monthly_budget=1500)
    tracker.add_expense(85.50, "Groceries", "Supermarket food")
    tracker.add_expense(45.00, "Transport", "Monthly bus pass")
    tracker.add_expense(120.00, "Utilities", "Electricity bill")
    tracker.add_expense(35.20, "Groceries", "Organic fruits")
    tracker.generate_report()''',
            'challenges': '* Export monthly summaries to formatted CSV spreadsheets.\n* Add alert warnings when a category exceeds 30% of total budget.'
        },
        {
            'title': 'Secure Password Generator & Vault',
            'slug': 'password-generator-and-vault',
            'level': 'intermediate',
            'order': 5,
            'description': 'A cryptographically secure password generator with customizable length, symbols, entropy calculation, and password strength evaluation.',
            'requirements': 'Python 3.9+\nStandard library secrets, string, and math modules',
            'concepts_used': 'Cryptographic Randomness (secrets module), String manipulation, Information Entropy calculation',
            'step_by_step_guide': '''### Step 1: Use secrets Instead of random
Standard `random` is pseudo-random and unsafe for passwords. Always use the `secrets` module for cryptographic safety.

### Step 2: Build Customizable Character Sets
Allow selecting lowercase, uppercase, digits, and special symbols.

### Step 3: Guarantee Constraint Inclusions
Ensure at least one character from each selected category is guaranteed in the generated password.

### Step 4: Calculate Password Entropy
Evaluate Shannon entropy in bits to give a strength rating (Weak, Moderate, Strong, Unbreakable).''',
            'source_code': '''import secrets
import string
import math

def generate_secure_password(length=16, use_upper=True, use_digits=True, use_symbols=True):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters for security.")

    chars = string.ascii_lowercase
    guaranteed = [secrets.choice(string.ascii_lowercase)]

    if use_upper:
        chars += string.ascii_uppercase
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        guaranteed.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}<>"
        chars += symbols
        guaranteed.append(secrets.choice(symbols))

    remaining_len = length - len(guaranteed)
    password_chars = guaranteed + [secrets.choice(chars) for _ in range(remaining_len)]
    
    # Secure shuffle
    secrets.SystemRandom().shuffle(password_chars)
    password = "".join(password_chars)
    
    # Calculate Shannon Entropy
    pool_size = len(chars)
    entropy_bits = length * math.log2(pool_size)
    
    return password, round(entropy_bits, 1)

if __name__ == "__main__":
    pwd, entropy = generate_secure_password(length=18)
    print(f"Generated Password: {pwd}")
    print(f"Entropy: {entropy} bits")
    rating = "Unbreakable 🛡️" if entropy > 80 else "Strong 🔒"
    print(f"Rating: {rating}")''',
            'challenges': '* Add integration with haveibeenpwned API (via k-anonymity SHA-1 hash) to verify if password has leaked.'
        },

        # --- ADVANCED ---
        {
            'title': 'RESTful API with Django & DRF',
            'slug': 'restful-api-django-drf',
            'level': 'advanced',
            'order': 6,
            'description': 'A production-grade REST API backend with Token Authentication, CRUD endpoints, query pagination, permission gates, and serializers.',
            'requirements': 'Django 5.0+\nDjango REST Framework\nSQLite or PostgreSQL',
            'concepts_used': 'MVT Architecture, DRF Serializers, ViewSets, JWT/Token Auth, Database Indexing, Unit Testing',
            'step_by_step_guide': '''### Step 1: Configure Models & Migrations
Design relational models with foreign keys, ordering, and indexed fields.

### Step 2: Implement ModelSerializers
Validate data payloads, sanitize fields, and serialize relationships.

### Step 3: Build ModelViewSets
Leverage DRF ViewSets for standardized list, retrieve, create, update, and destroy actions.

### Step 4: Add Authentication & Permissions
Enforce `IsAuthenticatedOrReadOnly` and custom ownership object-level permissions.

### Step 5: Test Endpoints
Write automated test cases checking HTTP 200, 201, 400, and 403 status codes.''',
            'source_code': '''# Reference architecture for Django REST Framework API
from rest_framework import serializers, viewsets, permissions
from django.db import models
from django.contrib.auth.models import User

# Model
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Serializer
class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Article
        fields = ["id", "title", "content", "author_username", "published", "created_at"]

# ViewSet
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True).select_related("author")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
''',
            'challenges': '* Implement Redis caching for the top read-heavy list endpoints.\n* Add Swagger / OpenAPI interactive documentation.'
        },
        {
            'title': 'High-Throughput File Organizer & Batch Processor',
            'slug': 'file-organizer-batch-processor',
            'level': 'advanced',
            'order': 7,
            'description': 'An automated file daemon that scans directories, classifies files by MIME type, extracts metadata, and sorts into organized directory trees.',
            'requirements': 'Python 3.9+\npathlib, hashlib, shutil standard modules',
            'concepts_used': 'Pathlib, SHA256 deduplication, File system operations, Metaprogramming, Logging',
            'step_by_step_guide': '''### Step 1: Directory Traversal
Use `pathlib.Path.rglob()` to recursively traverse messy directories.

### Step 2: Compute Hash Fingerprints
Hash file contents with SHA-256 to detect and eliminate duplicate files regardless of filename.

### Step 3: Categorize by Extension and MIME
Organize into categorized subdirectories (Documents, Images, Archives, Code, Media).

### Step 4: Safe Atomic Moves
Implement conflict resolution when target files with identical names already exist.''',
            'source_code': '''import hashlib
import os
from pathlib import Path
import shutil

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"]
}

def compute_sha256(filepath, chunk_size=65536):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def organize_directory(target_dir):
    target = Path(target_dir)
    if not target.exists():
        print("Directory does not exist.")
        return

    seen_hashes = {}
    duplicates = []
    
    print(f"Scanning {target.resolve()}...")
    for file_path in target.iterdir():
        if file_path.is_file():
            # Check for duplicates
            file_hash = compute_sha256(file_path)
            if file_hash in seen_hashes:
                duplicates.append((file_path, seen_hashes[file_hash]))
                continue
            seen_hashes[file_hash] = file_path

            # Determine category folder
            ext = file_path.suffix.lower()
            dest_category = "Other"
            for cat, extensions in CATEGORIES.items():
                if ext in extensions:
                    dest_category = cat
                    break

            category_folder = target / dest_category
            category_folder.mkdir(exist_ok=True)
            destination = category_folder / file_path.name
            
            # Atomic move
            shutil.move(str(file_path), str(destination))
            print(f"Moved: {file_path.name} -> {dest_category}/")

    print(f"Organization complete! Found {len(duplicates)} duplicate files.")

if __name__ == "__main__":
    print("Organizer engine ready.")
''',
            'challenges': '* Run this process as a background service listening for new file drop events via watchdog library.'
        }
    ]

    for p_data in projects_data:
        Project.objects.update_or_create(
            slug=p_data['slug'],
            defaults=p_data
        )

    print("Real Python Projects seeded successfully.")
