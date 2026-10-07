import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .sandbox import execute_python_code

def practice_view(request):
    """
    Renders the interactive Python online playground / compiler page.
    """
    sample_snippets = [
        {
            'name': 'Hello World & Variables',
            'code': 'name = "Python Explorer"\nage = 2026 - 1991\nprint(f"Welcome, {name}!")\nprint(f"Python has been empowering developers for {age} years.")'
        },
        {
            'name': 'Functions & Fibonacci',
            'code': 'def fibonacci(n):\n    sequence = [0, 1]\n    while len(sequence) < n:\n        sequence.append(sequence[-1] + sequence[-2])\n    return sequence[:n]\n\nprint("First 10 Fibonacci numbers:")\nprint(fibonacci(10))'
        },
        {
            'name': 'List Comprehension',
            'code': 'numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens_squared = [n**2 for n in numbers if n % 2 == 0]\nprint(f"Original: {numbers}")\nprint(f"Even squares: {evens_squared}")'
        },
        {
            'name': 'Object-Oriented Programming',
            'code': 'class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n\n    def get_grade(self):\n        if self.score >= 90: return "A"\n        elif self.score >= 75: return "B"\n        return "C"\n\ns = Student("Gowtham", 94)\nprint(f"{s.name}\'s grade: {s.get_grade()}")'
        }
    ]
    return render(request, 'practice/practice.html', {'sample_snippets': sample_snippets})

@api_view(['POST'])
@permission_classes([AllowAny])
def run_code_api(request):
    """
    API endpoint to securely execute arbitrary user Python code inside sandbox.
    """
    code = request.data.get('code', '')
    stdin_input = request.data.get('stdin', '')

    if not code.strip():
        return Response({
            'status': 'error',
            'stdout': '',
            'stderr': 'No code provided to execute.',
            'execution_time': 0.0
        })

    # Track streak for user if authenticated
    if request.user.is_authenticated:
        request.user.profile.update_streak()

    result = execute_python_code(code, stdin_input)
    return Response(result)
