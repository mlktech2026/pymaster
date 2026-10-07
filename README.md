# PyMaster - Interactive Python Learning Platform

A modern, responsive, full-featured Python learning website designed for beginners, intermediate, and advanced learners.

Built with **Python**, **Django 5**, **Django REST Framework**, **Tailwind CSS**, and **CodeMirror**, featuring a secure isolated code sandbox, automated exercise evaluator, interactive quizzes with countdown timers, visual roadmap, real-world portfolio projects, and a gamified badge & streak system.

---

## 🌟 Key Features

1. **66 Structured Python Tutorials**:
   - **Beginner Level (28 Topics)**: Installation, Syntax, Variables, Data Types, Numbers, Strings, Booleans, Operators, I/O, Conditionals (if, elif, else), Loops (for, while, break, continue, pass), Collections (Lists, Tuples, Sets, Dictionaries), Functions (arguments, return, scope, lambdas).
   - **Intermediate Level (23 Topics)**: List & Dictionary Comprehensions, Modules, Packages, Exception Handling, File I/O, JSON, Datetime, Regular Expressions, OOP (Classes, Objects, Constructors, Inheritance, Polymorphism, Encapsulation), Iterators, Generators, Decorators, Virtual Environments, pip, REST APIs.
   - **Advanced Level (15 Topics)**: Advanced OOP, Asyncio, Multithreading, Multiprocessing, Type Hints, Dataclasses, Unittest, Pytest, Logging, Project Structure, Database Programming, Django Web Development, REST APIs, Automation, Data Processing.
   - Each tutorial includes: Summary, Concept explanation, Syntax box, Python code example, Expected output, Important notes callout, Common mistakes callout, Real-world use case, and an embedded **Try It Yourself** interactive code editor.

2. **Dedicated Coding Exercises & Automated Test Runner**:
   - Filterable by difficulty: **Easy**, **Medium**, and **Hard**.
   - Dual-runner system:
     - **Run Tests**: Instantly tests solution against sample public test cases.
     - **Submit Solution**: Validates against all test cases (including hidden edge cases), calculates execution time, awards XP, and unlocks reference solutions and detailed explanations.

3. **Interactive Quizzes with Live Timer**:
   - Multiple question formats: Multiple Choice (MCQ), True/False, Code Output, and Fill in the Blank.
   - Live countdown timer, score calculation, letter grades (A+, A, B, C, F), pass/fail threshold, and complete answer review with explanations.

4. **Secure Isolated Code Sandbox**:
   - **Hardened Subprocess Isolation**: User code is executed in an isolated temporary worker process with `-I` isolated environment flags and stripped server environment variables.
   - **Execution Timeouts**: Enforced 4-second timeout to prevent infinite loops (`while True: pass`).
   - **AST Static Analysis**: Pre-execution AST scan intercepts forbidden modules (`subprocess`, sockets, system commands).
   - **Resource & Output Limits**: 64KB output buffer limits protect server memory.

5. **Gamification & Progress Tracking**:
   - **Daily Coding Streak** with streak freeze detection.
   - **XP / Points System** for lessons, exercises, and quizzes.
   - **Badges System**: *Python Beginner*, *First Exercise*, *First Quiz*, *10 Exercises Completed*, *50 Exercises Completed*, *Python Basics Completed*, *Quiz Master*, *7 Day Learning Streak*.
   - **Personalized Dashboard**: Overall course progress bar, 6 core metrics, "Continue Learning" last-lesson resume card, earned/locked badges shelf, and recent activity timeline.

6. **Interactive Visual Roadmap**:
   - Visual tiered roadmap connecting all 66 lessons across Beginner, Intermediate, and Advanced tiers.

7. **Real-world Python Projects**:
   - Beginner to Advanced portfolio projects (*CLI Calculator*, *Number Guessing Game*, *To-Do List*, *Personal Expense Tracker*, *Password Generator & Vault*, *RESTful API with Django*, *High-Throughput File Organizer*).
   - Each includes prerequisites, concepts used, architecture guide, copy-friendly full source code, and challenge extensions.

8. **Global Search**:
   - Searches across Tutorials, Exercises, Quizzes, and Projects with highlighted matching tags.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12, Django 5.x, Django REST Framework
- **Frontend**: HTML5, CSS3, Tailwind CSS (Dark/Light mode support), FontAwesome 6
- **Code Editor**: CodeMirror 5 with Python mode, Dracula theme, bracket matching
- **Database**: SQLite (local development) / PostgreSQL (production-ready)
- **Containerization**: Docker, Docker Compose

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Clone and Setup Environment
```bash
# Navigate to project folder
cd python_learning

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file (or copy `.env.example`):
```ini
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
SANDBOX_TIMEOUT_SECONDS=4
SANDBOX_MAX_OUTPUT_BYTES=65536
```

### 4. Run Migrations & Seed Database
```bash
# Apply migrations
python manage.py migrate

# Populate complete database (66 tutorials, exercises, quizzes, badges, projects, users)
python manage.py seed_data
```

### 5. Start Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
**http://127.0.0.1:8000/**

---

## 🔑 Pre-Configured Accounts

The `seed_data` command generates two default accounts:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `adminpassword123` | Full access to `/admin/` |
| **Learner** | `gowtham` | `python123` | Pre-initialized student profile |

---

## 🧪 Running Automated Tests

Run the comprehensive unit test suite:
```bash
python manage.py test core
```
Tests cover:
- Sandbox execution, timeouts, syntax errors, and AST security restrictions
- User registration, profiles, and streak updates
- Badge evaluation and award conditions
- View status codes and permission access control

---

## 🐳 Docker Deployment

To build and run with Docker:
```bash
docker-compose up --build
```
Access the application at `http://localhost:8000`.

---

## 📂 Project Structure

```text
python_learning/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
│
├── config/                  # Django project configuration & settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                # Authentication, profiles & streaks
├── tutorials/               # 66 Tutorials, categories, progress
├── exercises/               # Coding exercises, test runner, submissions
├── quizzes/                 # Multi-format quizzes, grading, answer review
├── practice/                # Online compiler & isolated sandbox execution
├── projects/                # Real-world portfolio project guides & source code
├── progress/                # Gamification, badges, user dashboard
├── core/                    # Homepage, roadmap, search, seed data commands
│
├── static/                  # CSS stylesheets, JS scripts, icons
└── templates/               # Responsive HTML templates with Tailwind CSS
```
"# pymaster" 
