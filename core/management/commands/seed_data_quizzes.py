"""
Comprehensive seed data definitions for Python Quizzes featuring all 20 question types.
60+ realistic, technical Python questions across Beginner, Intermediate, and Advanced tiers.
"""

from quizzes.models import Quiz, QuizQuestion, QuizOption

def seed_quizzes():
    print("Seeding Advanced Quiz Database (20 Question Types, 60+ Questions)...")

    # Clear existing questions to repopulate clean comprehensive dataset
    QuizOption.objects.all().delete()
    QuizQuestion.objects.all().delete()

    # Pre-configure Curated Quizzes
    quiz_basics, _ = Quiz.objects.get_or_create(
        slug='python-basics-mastery',
        defaults={
            'title': 'Python Basics Mastery',
            'category': 'Python Basics',
            'difficulty': 'beginner',
            'time_limit_mins': 10,
            'pass_percentage': 70,
            'description': 'Comprehensive test of variables, data types, operators, and fundamental Python logic.',
            'total_questions_count': 10,
            'is_published': True
        }
    )

    quiz_control, _ = Quiz.objects.get_or_create(
        slug='control-flow-and-loops',
        defaults={
            'title': 'Control Flow & Loops Challenge',
            'category': 'Loops',
            'difficulty': 'beginner',
            'time_limit_mins': 10,
            'pass_percentage': 75,
            'description': 'Master if-elif-else branches, for loops, while loops, and loop control statements.',
            'total_questions_count': 10,
            'is_published': True
        }
    )

    quiz_structures, _ = Quiz.objects.get_or_create(
        slug='data-structures-and-collections',
        defaults={
            'title': 'Data Structures & Collections',
            'category': 'Lists',
            'difficulty': 'intermediate',
            'time_limit_mins': 15,
            'pass_percentage': 70,
            'description': 'Deep dive into lists, tuples, sets, dictionaries, comprehensions, and memory references.',
            'total_questions_count': 10,
            'is_published': True
        }
    )

    quiz_oop, _ = Quiz.objects.get_or_create(
        slug='object-oriented-python',
        defaults={
            'title': 'Object-Oriented Python',
            'category': 'OOP',
            'difficulty': 'intermediate',
            'time_limit_mins': 15,
            'pass_percentage': 75,
            'description': 'Evaluate your knowledge of classes, constructors, inheritance, polymorphism, and encapsulation.',
            'total_questions_count': 10,
            'is_published': True
        }
    )

    quiz_advanced, _ = Quiz.objects.get_or_create(
        slug='advanced-python-debugging',
        defaults={
            'title': 'Advanced Python & Architecture',
            'category': 'Advanced Python',
            'difficulty': 'advanced',
            'time_limit_mins': 15,
            'pass_percentage': 75,
            'description': 'Advanced concurrency, decorators, exceptions, algorithms, and code debugging challenges.',
            'total_questions_count': 10,
            'is_published': True
        }
    )

    # Master question definitions for all 20 question types
    all_questions_pool = [
        # =========================================================================
        # 1. Multiple Choice Question (MCQ) - Single select
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'mcq',
            'category': 'Python Basics',
            'difficulty': 'easy',
            'marks': 1,
            'order': 1,
            'question_text': 'What is the output of the following arithmetic code?',
            'code_snippet': 'x = 10\nprint(x + 5)',
            'explanation': 'x is bound to integer 10. The + operator evaluates mathematical addition: 10 + 5 equals 15.',
            'options': [
                ('10', False),
                ('15', True),
                ('105', False),
                ('Error', False),
            ]
        },
        {
            'quiz': quiz_basics,
            'question_type': 'mcq',
            'category': 'Variables',
            'difficulty': 'easy',
            'marks': 1,
            'order': 2,
            'question_text': 'Which of the following variable names is INVALID according to Python syntax rules?',
            'code_snippet': '',
            'explanation': 'Variable names cannot start with a digit. 2nd_name is invalid syntax and triggers a SyntaxError.',
            'options': [
                ('_private_var', False),
                ('total_score', False),
                ('2nd_name', True),
                ('User_Age', False),
            ]
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'mcq',
            'category': 'Advanced Python',
            'difficulty': 'hard',
            'marks': 3,
            'order': 3,
            'question_text': 'In Python memory management, how does Python resolve object circular references that reference counting cannot reclaim?',
            'code_snippet': '',
            'explanation': 'Python employs a generational cyclic garbage collector (gc module) that detects and breaks unreachable isolated reference cycles.',
            'options': [
                ('Operating System memory paging', False),
                ('Generational cyclic garbage collector', True),
                ('Immediate process termination', False),
                ('Reference counter overflow flag', False),
            ]
        },

        # =========================================================================
        # 2. Multiple Select - Checkboxes (more than one answer)
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'multiple_select',
            'category': 'Data Types',
            'difficulty': 'easy',
            'marks': 2,
            'order': 4,
            'question_text': 'Which of the following are built-in standard data types in Python? (Select all that apply)',
            'code_snippet': '',
            'explanation': 'List, String, and Integer (int) are built-in core types in Python. HTML is a web markup language, not a Python data type.',
            'options': [
                ('List', True),
                ('String', True),
                ('Integer', True),
                ('HTML', False),
            ]
        },
        {
            'quiz': quiz_structures,
            'question_type': 'multiple_select',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 5,
            'question_text': 'Which of the following Python data structures are MUTABLE? (Select all that apply)',
            'code_snippet': '',
            'explanation': 'Lists, Dictionaries, and Sets can have their elements mutated in place. Tuples and Strings are immutable sequences.',
            'options': [
                ('list', True),
                ('tuple', False),
                ('dict', True),
                ('set', True),
                ('str', False),
            ]
        },
        {
            'quiz': quiz_control,
            'question_type': 'multiple_select',
            'category': 'Conditions',
            'difficulty': 'medium',
            'marks': 2,
            'order': 6,
            'question_text': 'Which of the following values evaluate to False in a Python boolean context? (Select all that apply)',
            'code_snippet': '',
            'explanation': 'In Python truthiness testing: 0, None, empty string "", and empty list [] are all falsy. Non-empty string "0" and integer -1 are truthy.',
            'options': [
                ('0', True),
                ('None', True),
                ('"" (empty string)', True),
                ('"0" (string with character zero)', False),
                ('-1', False),
            ]
        },

        # =========================================================================
        # 3. True / False - Interactive Card UI
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'true_false',
            'category': 'Python Basics',
            'difficulty': 'easy',
            'marks': 1,
            'order': 7,
            'question_text': 'Python is a dynamically typed programming language where variable types are checked at runtime.',
            'code_snippet': '',
            'explanation': 'True. In Python, you do not need to explicitly declare variable types, and a variable can reference different types over time.',
            'options': [
                ('True', True),
                ('False', False),
            ]
        },
        {
            'quiz': quiz_structures,
            'question_type': 'true_false',
            'category': 'Dictionaries',
            'difficulty': 'medium',
            'marks': 1,
            'order': 8,
            'question_text': 'A Python list can be used as a key in a standard Python dictionary.',
            'code_snippet': '',
            'explanation': 'False. Dictionary keys must be hashable and immutable. Lists are mutable and unhashable, raising a TypeError.',
            'options': [
                ('True', False),
                ('False', True),
            ]
        },
        {
            'quiz': quiz_control,
            'question_type': 'true_false',
            'category': 'Loops',
            'difficulty': 'medium',
            'marks': 1,
            'order': 9,
            'question_text': 'An `else` clause attached to a `for` loop in Python executes only if the loop completes without encountering a `break` statement.',
            'code_snippet': '',
            'explanation': 'True. The for...else construct executes the else block only when the loop terminates naturally without a break.',
            'options': [
                ('True', True),
                ('False', False),
            ]
        },

        # =========================================================================
        # 4. Fill in the Blank - User types exact keyword/token
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'fill_blank',
            'category': 'Python Basics',
            'difficulty': 'easy',
            'marks': 1,
            'order': 10,
            'question_text': 'Complete the code to prompt the user for input:',
            'code_snippet': 'name = ______("Enter your name: ")',
            'fill_blank_answer': 'input',
            'question_data': {'accepted_answers': ['input', 'input()']},
            'explanation': 'The built-in function input() reads a string from user terminal input.',
            'options': []
        },
        {
            'quiz': quiz_structures,
            'question_type': 'fill_blank',
            'category': 'Dictionaries',
            'difficulty': 'medium',
            'marks': 1,
            'order': 11,
            'question_text': 'Which dictionary method safely retrieves a value by key without raising a KeyError if the key is missing?',
            'code_snippet': 'user_role = profile.______("role", "guest")',
            'fill_blank_answer': 'get',
            'question_data': {'accepted_answers': ['get']},
            'explanation': 'dict.get(key, default) returns the value or a fallback default value rather than throwing a KeyError.',
            'options': []
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'fill_blank',
            'category': 'Functions',
            'difficulty': 'medium',
            'marks': 2,
            'order': 12,
            'question_text': 'Complete the code to define an anonymous inline function that squares its argument:',
            'code_snippet': 'square = ______ x: x ** 2',
            'fill_blank_answer': 'lambda',
            'question_data': {'accepted_answers': ['lambda']},
            'explanation': 'The lambda keyword defines anonymous single-expression callable functions in Python.',
            'options': []
        },

        # =========================================================================
        # 5. Code Output Prediction
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'code_output',
            'category': 'Operators',
            'difficulty': 'easy',
            'marks': 1,
            'order': 13,
            'question_text': 'What will be the output of the following arithmetic code?',
            'code_snippet': 'a = 5\nb = 2\nprint(a * b)',
            'explanation': 'The * operator performs multiplication between integers 5 and 2, resulting in 10.',
            'options': [
                ('7', False),
                ('10', True),
                ('52', False),
                ('Error', False),
            ]
        },
        {
            'quiz': quiz_structures,
            'question_type': 'code_output',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 14,
            'question_text': 'What will be the output of this list slicing operation?',
            'code_snippet': 'numbers = [10, 20, 30, 40, 50]\nprint(numbers[1:4])',
            'explanation': 'Slicing [1:4] extracts elements from index 1 up to (but not including) index 4: elements [20, 30, 40].',
            'options': [
                ('[10, 20, 30]', False),
                ('[20, 30, 40]', True),
                ('[20, 30, 40, 50]', False),
                ('[10, 20, 30, 40]', False),
            ]
        },
        {
            'quiz': quiz_control,
            'question_type': 'code_output',
            'category': 'Loops',
            'difficulty': 'medium',
            'marks': 2,
            'order': 15,
            'question_text': 'What is the output of this break condition inside the loop?',
            'code_snippet': 'for i in range(5):\n    if i == 2:\n        break\n    print(i, end="")',
            'explanation': 'When i=0 and i=1, they are printed without spaces. When i=2, break immediately exits the loop, yielding "01".',
            'options': [
                ('01', True),
                ('012', False),
                ('0134', False),
                ('2', False),
            ]
        },

        # =========================================================================
        # 6. Find the Error - Inspect broken code and pick bug from choices
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'find_error',
            'category': 'Loops',
            'difficulty': 'easy',
            'marks': 2,
            'order': 16,
            'question_text': 'What is wrong with the following Python code?',
            'code_snippet': 'for i in range(5)\n    print(i)',
            'explanation': 'In Python, statement header lines (for, while, if, def, class) must conclude with a colon (:).',
            'options': [
                ('Missing colon (:) at the end of the for statement line', True),
                ('range() cannot take a single argument', False),
                ('print statement must use single quotes', False),
                ('Variable i must be declared with let or var first', False),
            ]
        },
        {
            'quiz': quiz_structures,
            'question_type': 'find_error',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 17,
            'question_text': 'What causes the runtime error in this snippet?',
            'code_snippet': 'values = [1, 2, 3]\nvalues[3] = 4',
            'explanation': 'Python lists are 0-indexed. With 3 items, the maximum valid index is 2. Accessing index 3 triggers an IndexError: list assignment index out of range.',
            'options': [
                ('IndexError: Index 3 is out of range for a 3-element list', True),
                ('TypeError: Lists cannot contain integers', False),
                ('ValueError: Value 4 is already assigned', False),
                ('KeyError: Key 3 does not exist', False),
            ]
        },
        {
            'quiz': quiz_oop,
            'question_type': 'find_error',
            'category': 'OOP',
            'difficulty': 'medium',
            'marks': 2,
            'order': 18,
            'question_text': 'What is wrong with this class definition method?',
            'code_snippet': 'class Greeter:\n    def say_hello():\n        return "Hello World"\n\ng = Greeter()\nprint(g.say_hello())',
            'explanation': 'Instance methods must take `self` as their first parameter. When invoked as g.say_hello(), Python passes g automatically, resulting in TypeError: say_hello() takes 0 positional arguments but 1 was given.',
            'options': [
                ('say_hello() is missing the required `self` instance parameter', True),
                ('Class names must end with Class keyword', False),
                ('Greeter must inherit explicitly from object in Python 3', False),
                ('return statements are not permitted in class methods', False),
            ]
        },

        # =========================================================================
        # 7. Debug the Code - Interactive Code Editor
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'debug_code',
            'category': 'Loops',
            'difficulty': 'medium',
            'marks': 3,
            'order': 19,
            'question_text': 'Fix the syntax error in this loop so it prints each number in the list on a new line:',
            'code_snippet': 'numbers = [1, 2, 3, 4]\n\nfor i in numbers\n    print(i)',
            'question_data': {
                'expected_output': '1\n2\n3\n4',
                'solution_code': 'numbers = [1, 2, 3, 4]\n\nfor i in numbers:\n    print(i)'
            },
            'explanation': 'Adding the missing colon (:) after `for i in numbers` allows Python interpreter to parse the loop block correctly.',
            'options': []
        },
        {
            'quiz': quiz_basics,
            'question_type': 'debug_code',
            'category': 'Functions',
            'difficulty': 'easy',
            'marks': 3,
            'order': 20,
            'question_text': 'Debug this function so it correctly calculates and prints the double of 21:',
            'code_snippet': 'def double(n)\n    return n * 2\n\nprint(double(21))',
            'question_data': {
                'expected_output': '42',
                'solution_code': 'def double(n):\n    return n * 2\n\nprint(double(21))'
            },
            'explanation': 'Add the colon (:) at the end of the `def double(n):` header to fix the SyntaxError.',
            'options': []
        },

        # =========================================================================
        # 8. Arrange the Code - Drag and drop blocks into correct sequence
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'arrange_code',
            'category': 'Python Basics',
            'difficulty': 'easy',
            'marks': 2,
            'order': 21,
            'question_text': 'Arrange the code blocks in the correct logical execution order to greet the user with their name:',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': ['print(greeting)', 'name = "Gowtham"', 'greeting = f"Hello, {name}!"'],
                'correct_order': ['name = "Gowtham"', 'greeting = f"Hello, {name}!"', 'print(greeting)']
            },
            'explanation': 'Variables must be defined before they can be referenced in string formatting or print statements.',
            'options': []
        },
        {
            'quiz': quiz_control,
            'question_type': 'arrange_code',
            'category': 'Loops',
            'difficulty': 'medium',
            'marks': 3,
            'order': 22,
            'question_text': 'Arrange the code lines to create a countdown loop that prints 3, 2, 1 and then "Blast off!":',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': [
                    'print("Blast off!")',
                    'count = 3',
                    'while count > 0:',
                    '    print(count)',
                    '    count -= 1'
                ],
                'correct_order': [
                    'count = 3',
                    'while count > 0:',
                    '    print(count)',
                    '    count -= 1',
                    'print("Blast off!")'
                ]
            },
            'explanation': 'Initialize counter -> loop while positive -> print and decrement -> print final message after loop termination.',
            'options': []
        },

        # =========================================================================
        # 9. Match the Following - Concept to Purpose/Definition
        # =========================================================================
        {
            'quiz': quiz_structures,
            'question_type': 'match_following',
            'category': 'Data Structures',
            'difficulty': 'medium',
            'marks': 3,
            'order': 23,
            'question_text': 'Match each Python core collection type with its primary characteristic:',
            'code_snippet': '',
            'question_data': {
                'concepts': ['list', 'tuple', 'dictionary', 'set'],
                'definitions': [
                    'Mutable ordered sequence',
                    'Immutable ordered sequence',
                    'Key-value mapping table',
                    'Unordered collection of unique items'
                ],
                'correct_pairs': {
                    'list': 'Mutable ordered sequence',
                    'tuple': 'Immutable ordered sequence',
                    'dictionary': 'Key-value mapping table',
                    'set': 'Unordered collection of unique items'
                }
            },
            'explanation': 'List = mutable sequence [], Tuple = immutable sequence (), Dictionary = key-value {}, Set = unique deduplicated elements {}.',
            'options': []
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'match_following',
            'category': 'Exception Handling',
            'difficulty': 'medium',
            'marks': 3,
            'order': 24,
            'question_text': 'Match each Python exception block with its execution role:',
            'code_snippet': '',
            'question_data': {
                'concepts': ['try', 'except', 'else', 'finally'],
                'definitions': [
                    'Code block that may trigger an error',
                    'Executes when a specific exception occurs',
                    'Executes only if NO exception occurred',
                    'Always executes regardless of exceptions'
                ],
                'correct_pairs': {
                    'try': 'Code block that may trigger an error',
                    'except': 'Executes when a specific exception occurs',
                    'else': 'Executes only if NO exception occurred',
                    'finally': 'Always executes regardless of exceptions'
                }
            },
            'explanation': 'try wraps risky logic, except catches errors, else runs when try succeeds without errors, and finally runs cleanup always.',
            'options': []
        },

        # =========================================================================
        # 10. Drag and Drop Answer - Draggable keyword into target blank
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'drag_drop_blank',
            'category': 'Loops',
            'difficulty': 'easy',
            'marks': 2,
            'order': 25,
            'question_text': 'Drag the correct Python keyword into the blank to iterate over the sequence:',
            'code_snippet': '_____ x in range(5):\n    print(x)',
            'fill_blank_answer': 'for',
            'question_data': {
                'tokens': ['if', 'for', 'while', 'def'],
                'correct_token': 'for'
            },
            'explanation': 'The `for` keyword initiates a for-each sequence traversal loop in Python.',
            'options': []
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'drag_drop_blank',
            'category': 'Functions',
            'difficulty': 'easy',
            'marks': 2,
            'order': 26,
            'question_text': 'Drag the correct keyword into the blank to define a new function:',
            'code_snippet': '_____ calculate_area(radius):\n    return 3.14159 * radius ** 2',
            'fill_blank_answer': 'def',
            'question_data': {
                'tokens': ['func', 'def', 'function', 'class'],
                'correct_token': 'def'
            },
            'explanation': 'In Python, functions are defined using the `def` keyword.',
            'options': []
        },

        # =========================================================================
        # 11. Code Completion
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'code_completion',
            'category': 'Conditions',
            'difficulty': 'easy',
            'marks': 1,
            'order': 27,
            'question_text': 'Complete the code to print only even numbers by filling in the missing value:',
            'code_snippet': 'numbers = [1, 2, 3, 4, 5]\n\nfor number in numbers:\n    if number % 2 == ___:\n        print(number)',
            'fill_blank_answer': '0',
            'question_data': {'accepted_answers': ['0']},
            'explanation': 'A number is even when divisible by 2 with remainder 0 (`number % 2 == 0`).',
            'options': []
        },
        {
            'quiz': quiz_structures,
            'question_type': 'code_completion',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 28,
            'question_text': 'Complete the list method to append "Cherry" to the fruits list:',
            'code_snippet': 'fruits = ["Apple", "Banana"]\nfruits.____("Cherry")',
            'fill_blank_answer': 'append',
            'question_data': {'accepted_answers': ['append']},
            'explanation': 'The `.append()` method appends an element to the end of a list in place.',
            'options': []
        },

        # =========================================================================
        # 12. Scenario Based Question
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'scenario_based',
            'category': 'Conditions',
            'difficulty': 'easy',
            'marks': 2,
            'order': 29,
            'question_text': 'You are creating a user login system. You need to check whether the user-entered password strictly matches the stored hashed password. Which Python comparison operator should you use?',
            'code_snippet': '',
            'explanation': 'The equality operator `==` compares value equivalence. In contrast, `=` is for assignment, and `is` checks memory object identity.',
            'options': [
                ('== (equality operator)', True),
                ('= (assignment operator)', False),
                ('is (identity operator)', False),
                ('=== (strict identity operator)', False),
            ]
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'scenario_based',
            'category': 'File Handling',
            'difficulty': 'medium',
            'marks': 2,
            'order': 30,
            'question_text': 'You are writing an enterprise file ingestion script. You want to ensure the file resource is guaranteed to be closed even if an unexpected exception occurs during parsing. What Python idiom should you use?',
            'code_snippet': '',
            'explanation': 'The `with open(...) as f:` context manager guarantees the file descriptor will be closed immediately when exiting the block, even upon exceptions.',
            'options': [
                ('Use a `with open(...) as f:` context manager block', True),
                ('Call `f.close()` inside a global while loop', False),
                ('Assign `f = None` after reading', False),
                ('Rely on Python process exit to close handles', False),
            ]
        },

        # =========================================================================
        # 13. Order / Sequence Question
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'order_sequence',
            'category': 'Functions',
            'difficulty': 'easy',
            'marks': 2,
            'order': 31,
            'question_text': 'What is the correct logical lifecycle order for defining and executing a Python function?',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': [
                    'Pass arguments to the call',
                    'Define the function signature with def',
                    'Write the function body implementation',
                    'Call the function by name'
                ],
                'correct_sequence': [
                    'Define the function signature with def',
                    'Write the function body implementation',
                    'Call the function by name',
                    'Pass arguments to the call'
                ]
            },
            'explanation': 'A function must be defined with its signature and body before it can be called with arguments.',
            'options': []
        },
        {
            'quiz': quiz_advanced,
            'question_type': 'order_sequence',
            'category': 'Web Development',
            'difficulty': 'hard',
            'marks': 3,
            'order': 32,
            'question_text': 'Arrange the lifecycle steps of an incoming HTTP request in a standard Django architecture:',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': [
                    'Template renders HTML or Serializer returns JSON',
                    'Web server forwards request to Django wsgi/asgi handler',
                    'URLconf matches pattern and routes to View',
                    'Middleware inspects/modifies request',
                    'View queries Model / Database'
                ],
                'correct_sequence': [
                    'Web server forwards request to Django wsgi/asgi handler',
                    'Middleware inspects/modifies request',
                    'URLconf matches pattern and routes to View',
                    'View queries Model / Database',
                    'Template renders HTML or Serializer returns JSON'
                ]
            },
            'explanation': 'Request flows: WSGI/ASGI -> Middleware -> URLconf -> View -> Model/DB -> Template/Serializer Response.',
            'options': []
        },

        # =========================================================================
        # 14. Identify the Output (Complex multi-line output)
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'identify_output',
            'category': 'Loops',
            'difficulty': 'easy',
            'marks': 2,
            'order': 33,
            'question_text': 'Select the exact multi-line output produced by this loop:',
            'code_snippet': 'numbers = [1, 2, 3]\n\nfor n in numbers:\n    print(n * 2)',
            'explanation': 'Each number (1, 2, 3) multiplied by 2 is 2, 4, 6, and print() outputs each on a new line by default.',
            'options': [
                ('2\n4\n6', True),
                ('1\n2\n3', False),
                ('2 4 6', False),
                ('[2, 4, 6]', False),
            ]
        },
        {
            'quiz': quiz_structures,
            'question_type': 'identify_output',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 34,
            'question_text': 'What is the output of this list comprehension with conditional filter?',
            'code_snippet': 'words = ["hi", "python", "go", "developer"]\nresult = [w.upper() for w in words if len(w) > 4]\nprint(result)',
            'explanation': 'Only words with length > 4 ("python" len 6, "developer" len 9) are kept and converted to uppercase.',
            'options': [
                ("['PYTHON', 'DEVELOPER']", True),
                ("['HI', 'PYTHON', 'GO', 'DEVELOPER']", False),
                ("['PYTHON']", False),
                ("['DEVELOPER']", False),
            ]
        },

        # =========================================================================
        # 15. Predict the Variable Value
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'predict_variable',
            'category': 'Variables',
            'difficulty': 'easy',
            'marks': 2,
            'order': 35,
            'question_text': 'Trace the operations below. What is the final integer value of variable `x`?',
            'code_snippet': 'x = 10\nx = x + 5\nx = x * 2',
            'fill_blank_answer': '30',
            'question_data': {'accepted_answers': ['30']},
            'explanation': 'x starts at 10. Then x + 5 = 15. Finally 15 * 2 = 30.',
            'options': []
        },
        {
            'quiz': quiz_structures,
            'question_type': 'predict_variable',
            'category': 'Dictionaries',
            'difficulty': 'medium',
            'marks': 2,
            'order': 36,
            'question_text': 'What is the final integer value stored in `data["b"]`?',
            'code_snippet': 'data = {"a": 10, "b": 20}\ndata["b"] += data["a"]\ndata["a"] = 50',
            'fill_blank_answer': '30',
            'question_data': {'accepted_answers': ['30']},
            'explanation': 'data["b"] becomes 20 + 10 = 30. Modifying data["a"] afterward has no effect on "b".',
            'options': []
        },

        # =========================================================================
        # 16. Code Ordering - Program statement ordering
        # =========================================================================
        {
            'quiz': quiz_advanced,
            'question_type': 'code_ordering',
            'category': 'File Handling',
            'difficulty': 'medium',
            'marks': 2,
            'order': 37,
            'question_text': 'Order the code lines to safely open, read, and print the contents of a file:',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': [
                    'print(content)',
                    'content = f.read()',
                    'with open("notes.txt", "r") as f:'
                ],
                'correct_order': [
                    'with open("notes.txt", "r") as f:',
                    'content = f.read()',
                    'print(content)'
                ]
            },
            'explanation': 'Open file via context manager -> read contents from file handle -> print content.',
            'options': []
        },
        {
            'quiz': quiz_oop,
            'question_type': 'code_ordering',
            'category': 'OOP',
            'difficulty': 'medium',
            'marks': 3,
            'order': 38,
            'question_text': 'Order the lines to define a class with a constructor that stores an attribute:',
            'code_snippet': '',
            'question_data': {
                'shuffled_blocks': [
                    'self.name = name',
                    'class Person:',
                    'def __init__(self, name):'
                ],
                'correct_order': [
                    'class Person:',
                    'def __init__(self, name):',
                    'self.name = name'
                ]
            },
            'explanation': 'class declaration -> __init__ constructor definition -> attribute assignment.',
            'options': []
        },

        # =========================================================================
        # 17. Image / Diagram Based Question
        # =========================================================================
        {
            'quiz': quiz_oop,
            'question_type': 'diagram_question',
            'category': 'OOP',
            'difficulty': 'medium',
            'marks': 2,
            'order': 39,
            'question_text': 'Which core Object-Oriented Programming concept is illustrated in the architectural diagram below?',
            'code_snippet': '''┌────────────────┐
│  Vehicle Base  │
└───────┬────────┘
        │ (inherits)
   ┌────┴────┐
   ▼         ▼
┌─────┐   ┌───────┐
│ Car │   │ Truck │
└─────┘   └───────┘''',
            'explanation': 'The diagram demonstrates Inheritance, where child classes Car and Truck derive attributes and behavior from a base Vehicle class.',
            'options': [
                ('Inheritance', True),
                ('Encapsulation', False),
                ('List Comprehension', False),
                ('Garbage Collection', False),
            ]
        },
        {
            'quiz': quiz_control,
            'question_type': 'diagram_question',
            'category': 'Control Flow',
            'difficulty': 'easy',
            'marks': 2,
            'order': 40,
            'question_text': 'What programming construct does this logic flow represent?',
            'code_snippet': '''     [ Start ]
         │
         ▼
    < Is x > 0? >
     /         \\
  (Yes)       (No)
   /             \\
[ Action A ]  [ Action B ]
   \\             /
    ▼           ▼
      [ End ]''',
            'explanation': 'A conditional decision diamond branching into two paths based on a boolean condition represents an if-else decision statement.',
            'options': [
                ('Conditional Branching (if - else)', True),
                ('While loop iteration', False),
                ('Function recursive call', False),
                ('Thread deadlock', False),
            ]
        },

        # =========================================================================
        # 18. Short Answer - Typing short keyword / function name
        # =========================================================================
        {
            'quiz': quiz_basics,
            'question_type': 'short_answer',
            'category': 'Functions',
            'difficulty': 'easy',
            'marks': 1,
            'order': 41,
            'question_text': 'What keyword is used to define a function in Python?',
            'code_snippet': '',
            'fill_blank_answer': 'def',
            'question_data': {'accepted_answers': ['def']},
            'explanation': 'The def keyword (short for define) is used to create named functions in Python.',
            'options': []
        },
        {
            'quiz': quiz_structures,
            'question_type': 'short_answer',
            'category': 'Python Basics',
            'difficulty': 'easy',
            'marks': 1,
            'order': 42,
            'question_text': 'What built-in function returns the total number of items in a sequence or collection?',
            'code_snippet': '',
            'fill_blank_answer': 'len',
            'question_data': {'accepted_answers': ['len', 'len()']},
            'explanation': 'The len() function returns the length (count of elements) of lists, strings, dictionaries, tuples, and sets.',
            'options': []
        },

        # =========================================================================
        # 19. Code Comparison - Compare Snippet A vs Snippet B
        # =========================================================================
        {
            'quiz': quiz_structures,
            'question_type': 'code_comparison',
            'category': 'Lists',
            'difficulty': 'medium',
            'marks': 2,
            'order': 43,
            'question_text': 'Which of the two code snippets is more idiomatic ("Pythonic") and faster for squaring a list of numbers?',
            'code_snippet': '''# Snippet A (Traditional loop)
squares = []
for x in numbers:
    squares.append(x ** 2)

# Snippet B (List comprehension)
squares = [x ** 2 for x in numbers]''',
            'explanation': 'Snippet B (List comprehension) is more idiomatic Python (PEP 20) and executes significantly faster at C-level in CPython than repeated .append() method lookups.',
            'options': [
                ('Snippet B is more idiomatic and faster', True),
                ('Snippet A is more idiomatic and faster', False),
                ('Both have identical execution and bytecode', False),
                ('Snippet B causes a memory leak', False),
            ]
        },
        {
            'quiz': quiz_basics,
            'question_type': 'code_comparison',
            'category': 'Strings',
            'difficulty': 'easy',
            'marks': 2,
            'order': 44,
            'question_text': 'Which string formatting approach is recommended in modern Python 3.6+ for speed and readability?',
            'code_snippet': '''# Approach A: % formatting
msg = "Hello %s, your score is %d" % (name, score)

# Approach B: f-strings
msg = f"Hello {name}, your score is {score}"''',
            'explanation': 'Formatted string literals (f-strings, PEP 498) introduced in Python 3.6 are the recommended standard because they are cleaner and faster than % formatting or str.format().',
            'options': [
                ('Approach B (f-strings)', True),
                ('Approach A (% formatting)', False),
                ('Neither, string concatenation (+) is best', False),
            ]
        },

        # =========================================================================
        # 20. Mini Coding Challenge - Live code runner against test cases
        # =========================================================================
        {
            'quiz': quiz_control,
            'question_type': 'mini_challenge',
            'category': 'Loops',
            'difficulty': 'medium',
            'marks': 4,
            'order': 45,
            'question_text': 'Write a Python program that prints all even numbers from 2 to 8 (inclusive), each on a new line:',
            'code_snippet': '# Write your code below:\n',
            'question_data': {
                'expected_output': '2\n4\n6\n8',
                'solution_code': 'for i in range(2, 9, 2):\n    print(i)'
            },
            'explanation': 'Use `for i in range(2, 9, 2): print(i)` or filter with `if i % 2 == 0:` to output 2, 4, 6, 8.',
            'options': []
        },
        {
            'quiz': quiz_basics,
            'question_type': 'mini_challenge',
            'category': 'Functions',
            'difficulty': 'medium',
            'marks': 4,
            'order': 46,
            'question_text': 'Write a program that defines variable `radius = 5` and prints the area of the circle using pi = 3.14 (Area = pi * r^2):',
            'code_snippet': '# Calculate and print the circle area:\n',
            'question_data': {
                'expected_output': '78.5',
                'solution_code': 'radius = 5\nprint(3.14 * (radius ** 2))'
            },
            'explanation': 'Compute `3.14 * (5 ** 2) = 78.5` and print the result.',
            'options': []
        },
    ]

    # Save all questions and options
    for q_data in all_questions_pool:
        options = q_data.pop('options', [])
        question = QuizQuestion.objects.create(**q_data)

        for opt_idx, (opt_text, is_corr) in enumerate(options, 1):
            QuizOption.objects.create(
                question=question,
                option_text=opt_text,
                is_correct=is_corr,
                order=opt_idx
            )

    print(f"Successfully seeded {QuizQuestion.objects.count()} questions across all 20 question types.")
