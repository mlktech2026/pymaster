"""
Seed data definitions for Python Exercises across Easy, Medium, and Hard difficulty tiers.
"""

from exercises.models import ExerciseCategory, Exercise, ExerciseTestCase

def seed_exercises():
    print("Seeding Exercises & Test Cases...")

    # Categories
    cat_basics, _ = ExerciseCategory.objects.get_or_create(
        slug='variables-and-control',
        defaults={'name': 'Basics & Control Flow', 'icon': 'fa-code-branch', 'description': 'Variables, operators, conditions, and loops.'}
    )
    cat_collections, _ = ExerciseCategory.objects.get_or_create(
        slug='strings-and-lists',
        defaults={'name': 'Strings & Collections', 'icon': 'fa-list-ol', 'description': 'Strings, lists, and dictionary manipulation.'}
    )
    cat_functions, _ = ExerciseCategory.objects.get_or_create(
        slug='functions-and-logic',
        defaults={'name': 'Functions & Logic', 'icon': 'fa-gears', 'description': 'Functions, recursion, and algorithm problems.'}
    )
    cat_oop, _ = ExerciseCategory.objects.get_or_create(
        slug='oop-and-design',
        defaults={'name': 'OOP & Architecture', 'icon': 'fa-sitemap', 'description': 'Classes, inheritance, and real-world domain problems.'}
    )
    cat_data, _ = ExerciseCategory.objects.get_or_create(
        slug='data-and-algorithms',
        defaults={'name': 'Data & Algorithms', 'icon': 'fa-brain', 'description': 'Data transformations, sorting, and optimization.'}
    )

    exercises_data = [
        # --- EASY ---
        {
            'category': cat_basics,
            'title': 'Find Even Numbers',
            'slug': 'find-even-numbers',
            'difficulty': 'easy',
            'points': 10,
            'order': 1,
            'description': 'Given a list of integers, iterate through the numbers and print only the even numbers, each on a new line.\n\n### Requirements:\n* Use a loop to inspect each number.\n* Use the modulus operator `%` to determine if a number is divisible by 2.',
            'example_input': 'numbers = [10, 15, 20, 25, 30]',
            'example_output': '10\n20\n30',
            'hints': 'Remember: a number `n` is even if `n % 2 == 0`.',
            'explanation': 'We iterate through `numbers` using a `for` loop. For each integer, `if n % 2 == 0:` evaluates to True when divisible by 2 with no remainder, printing only the even values.',
            'starter_code': 'numbers = [10, 15, 20, 25, 30]\n\n# Write your code below to print only even numbers:\n',
            'solution_code': 'numbers = [10, 15, 20, 25, 30]\nfor n in numbers:\n    if n % 2 == 0:\n        print(n)',
            'test_cases': [
                {'input_data': '', 'expected_output': '10\n20\n30', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_basics,
            'title': 'Sum of Natural Numbers',
            'slug': 'sum-of-natural-numbers',
            'difficulty': 'easy',
            'points': 10,
            'order': 2,
            'description': 'Calculate and print the sum of all integers from 1 up to 10 inclusive.\n\n### Output Format:\nPrint single integer representing the total sum.',
            'example_input': 'Range: 1 to 10',
            'example_output': '55',
            'hints': 'You can use `range(1, 11)` and Python\'s built-in `sum()` function, or a `for` loop.',
            'explanation': 'The sum of natural numbers from 1 to 10 is (10 * 11) / 2 = 55.',
            'starter_code': '# Compute the sum of integers from 1 to 10 inclusive\ntotal = 0\n# Your code here:\n\nprint(total)',
            'solution_code': 'total = sum(range(1, 11))\nprint(total)',
            'test_cases': [
                {'input_data': '', 'expected_output': '55', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_collections,
            'title': 'Reverse a String',
            'slug': 'reverse-a-string',
            'difficulty': 'easy',
            'points': 10,
            'order': 3,
            'description': 'Given string variable `text = "Python"`, print the reversed string.\n\n### Output:\n`nohtyP`',
            'example_input': 'text = "Python"',
            'example_output': 'nohtyP',
            'hints': 'Python slice notation supports step syntax: `string[::-1]`.',
            'explanation': 'Using slice syntax `[::-1]` steps through the sequence backward from the last element to the first, creating a reversed copy.',
            'starter_code': 'text = "Python"\n# Reverse and print text:\n',
            'solution_code': 'text = "Python"\nprint(text[::-1])',
            'test_cases': [
                {'input_data': '', 'expected_output': 'nohtyP', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_collections,
            'title': 'Count Vowels in String',
            'slug': 'count-vowels-in-string',
            'difficulty': 'easy',
            'points': 15,
            'order': 4,
            'description': 'Count the total number of vowels (a, e, i, o, u - case insensitive) in the sentence:\n`phrase = "Artificial Intelligence and Machine Learning"`\n\nPrint the total integer count.',
            'example_input': 'phrase = "Artificial Intelligence and Machine Learning"',
            'example_output': '18',
            'hints': 'Convert phrase to lowercase with `.lower()` and check if each character is in `"aeiou"`.',
            'explanation': 'Loop over characters in `phrase.lower()` and increment a counter if the character is in the vowel set.',
            'starter_code': 'phrase = "Artificial Intelligence and Machine Learning"\nvowels = "aeiou"\ncount = 0\n\n# Your code here:\n\nprint(count)',
            'solution_code': 'phrase = "Artificial Intelligence and Machine Learning"\nvowels = "aeiou"\ncount = sum(1 for ch in phrase.lower() if ch in vowels)\nprint(count)',
            'test_cases': [
                {'input_data': '', 'expected_output': '18', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_basics,
            'title': 'FizzBuzz',
            'slug': 'fizz-buzz',
            'difficulty': 'easy',
            'points': 15,
            'order': 5,
            'description': 'For numbers from 1 to 15 (inclusive):\n* If divisible by 3 and 5, print "FizzBuzz"\n* If divisible by 3, print "Fizz"\n* If divisible by 5, print "Buzz"\n* Otherwise, print the number itself.',
            'example_input': 'Range 1 to 15',
            'example_output': '1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz',
            'hints': 'Always check `i % 15 == 0` first before checking 3 and 5 independently!',
            'explanation': 'Because numbers divisible by 15 are also divisible by 3 and 5, evaluating the combined condition first prevents premature single branches.',
            'starter_code': '# Write a loop from 1 to 15 implementing FizzBuzz:\n',
            'solution_code': 'for i in range(1, 16):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)',
            'test_cases': [
                {'input_data': '', 'expected_output': '1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz', 'is_sample': True, 'order': 1},
            ]
        },

        # --- MEDIUM ---
        {
            'category': cat_functions,
            'title': 'Palindrome Checker Function',
            'slug': 'palindrome-checker-function',
            'difficulty': 'medium',
            'points': 20,
            'order': 6,
            'description': 'Define a function `is_palindrome(s)` that returns `True` if a given string is a palindrome (ignoring spaces, punctuation, and letter case), and `False` otherwise.\n\nTest with:\n1. `"Racecar"` -> True\n2. `"A man a plan a canal Panama"` -> True\n3. `"Python"` -> False',
            'example_input': 'is_palindrome("Racecar")',
            'example_output': 'True\nTrue\nFalse',
            'hints': 'Clean the string by keeping only alphanumeric characters using `ch.isalnum()` and `.lower()`.',
            'explanation': 'Filtering the characters with `[ch.lower() for ch in s if ch.isalnum()]` normalizes the input before checking if the list equals its reverse.',
            'starter_code': 'def is_palindrome(s):\n    # Return True if palindrome, False otherwise\n    pass\n\nprint(is_palindrome("Racecar"))\nprint(is_palindrome("A man a plan a canal Panama"))\nprint(is_palindrome("Python"))',
            'solution_code': 'def is_palindrome(s):\n    cleaned = [ch.lower() for ch in s if ch.isalnum()]\n    return cleaned == cleaned[::-1]\n\nprint(is_palindrome("Racecar"))\nprint(is_palindrome("A man a plan a canal Panama"))\nprint(is_palindrome("Python"))',
            'test_cases': [
                {'input_data': '', 'expected_output': 'True\nTrue\nFalse', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_collections,
            'title': 'Word Frequency Counter',
            'slug': 'word-frequency-counter',
            'difficulty': 'medium',
            'points': 20,
            'order': 7,
            'description': 'Given a paragraph of text, count the frequency of each unique word (lowercase, stripped of punctuation). Print the top 3 most common words and their counts in the format: `word: count`.\n\nSentence:\n`"python is fun and python is powerful and python is fast"`',
            'example_input': 'text = "python is fun and python is powerful and python is fast"',
            'example_output': 'python: 3\nis: 3\nand: 2',
            'hints': 'Split into words, use a dictionary or `collections.Counter`, and sort by frequency descending.',
            'explanation': 'Counter from collections tallies word occurrences in O(n) time, and `.most_common(3)` retrieves the top frequencies.',
            'starter_code': 'text = "python is fun and python is powerful and python is fast"\n\n# Count word frequencies and print top 3 as "word: count":\n',
            'solution_code': 'from collections import Counter\ntext = "python is fun and python is powerful and python is fast"\ncounts = Counter(text.split())\nfor word, count in counts.most_common(3):\n    print(f"{word}: {count}")',
            'test_cases': [
                {'input_data': '', 'expected_output': 'python: 3\nis: 3\nand: 2', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_collections,
            'title': 'List Comprehension Filtering & Squaring',
            'slug': 'list-comprehension-filter',
            'difficulty': 'medium',
            'points': 20,
            'order': 8,
            'description': 'Given a list of integers from 1 to 20, write a single list comprehension that squares all numbers that are multiples of 3, and print the resulting list.',
            'example_input': 'range(1, 21)',
            'example_output': '[9, 36, 81, 144, 225, 324]',
            'hints': 'The syntax is `[x**2 for x in range(1, 21) if x % 3 == 0]`.',
            'explanation': 'Multiples of 3 in 1..20 are [3, 6, 9, 12, 15, 18]. Their squares are 9, 36, 81, 144, 225, 324.',
            'starter_code': '# Write a single list comprehension:\nresult = None\nprint(result)',
            'solution_code': 'result = [x**2 for x in range(1, 21) if x % 3 == 0]\nprint(result)',
            'test_cases': [
                {'input_data': '', 'expected_output': '[9, 36, 81, 144, 225, 324]', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_oop,
            'title': 'BankAccount Class with Validation',
            'slug': 'bank-account-class',
            'difficulty': 'medium',
            'points': 25,
            'order': 9,
            'description': 'Create a class `BankAccount` with:\n* Constructor `__init__(self, owner, balance=0)`\n* Method `deposit(self, amount)` that adds to balance and returns current balance\n* Method `withdraw(self, amount)`: if sufficient funds exist, deducts amount and returns current balance; if insufficient funds, prints `"Insufficient funds"` and returns current balance\n\nRun the following operations:\n```python\nacc = BankAccount("Gowtham", 100)\nacc.deposit(50)\nacc.withdraw(120)\nacc.withdraw(50)\nprint("Final balance:", acc.balance)\n```',
            'example_input': 'Deposit 50, withdraw 120, withdraw 50 from starting balance 100',
            'example_output': 'Insufficient funds\nFinal balance: 30',
            'hints': 'Check `if amount > self.balance` before withdrawing.',
            'explanation': 'State encapsulation ensures balance cannot be directly mutated without validation safeguards.',
            'starter_code': 'class BankAccount:\n    # Implement constructor, deposit, and withdraw:\n    pass\n\nacc = BankAccount("Gowtham", 100)\nacc.deposit(50)\nacc.withdraw(120)\nacc.withdraw(50)\nprint("Final balance:", acc.balance)',
            'solution_code': 'class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            print("Insufficient funds")\n            return self.balance\n        self.balance -= amount\n        return self.balance\n\nacc = BankAccount("Gowtham", 100)\nacc.deposit(50)\nacc.withdraw(120)\nacc.withdraw(50)\nprint("Final balance:", acc.balance)',
            'test_cases': [
                {'input_data': '', 'expected_output': 'Insufficient funds\nFinal balance: 30', 'is_sample': True, 'order': 1},
            ]
        },

        # --- HARD ---
        {
            'category': cat_data,
            'title': 'Two Sum Problem',
            'slug': 'two-sum-problem',
            'difficulty': 'hard',
            'points': 30,
            'order': 10,
            'description': 'Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target` in O(n) time complexity.\n\nPrint the sorted pair of indices as `[i, j]`.\n\nExample:\n`nums = [2, 7, 11, 15]`, `target = 9` -> Output: `[0, 1]`\n`nums = [3, 2, 4]`, `target = 6` -> Output: `[1, 2]`',
            'example_input': 'nums = [2, 7, 11, 15], target = 9',
            'example_output': '[0, 1]\n[1, 2]',
            'hints': 'Use a hash map (dictionary) storing `seen[number] = index` to find the complement `target - num` in O(1) time.',
            'explanation': 'For each number `n`, the complement `target - n` is checked against the hash map. If present, the pair is found in one pass.',
            'starter_code': 'def two_sum(nums, target):\n    # Solve in O(n) using a dictionary:\n    pass\n\nprint(two_sum([2, 7, 11, 15], 9))\nprint(two_sum([3, 2, 4], 6))',
            'solution_code': 'def two_sum(nums, target):\n    seen = {}\n    for idx, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return sorted([seen[diff], idx])\n        seen[num] = idx\n    return []\n\nprint(two_sum([2, 7, 11, 15], 9))\nprint(two_sum([3, 2, 4], 6))',
            'test_cases': [
                {'input_data': '', 'expected_output': '[0, 1]\n[1, 2]', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_functions,
            'title': 'Custom Memoization Decorator',
            'slug': 'custom-memoization-decorator',
            'difficulty': 'hard',
            'points': 30,
            'order': 11,
            'description': 'Build a custom decorator `@memoize` that caches function outputs based on input arguments.\n\nTest with a recursive Fibonacci function `fib(n)`:\n```python\n@memoize\ndef fib(n):\n    if n < 2: return n\n    return fib(n - 1) + fib(n - 2)\n\nprint([fib(i) for i in range(10)])\n```',
            'example_input': 'fib(i) for i in range(10)',
            'example_output': '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]',
            'hints': 'Create a cache dictionary inside the decorator wrapper and check `if args in cache`.',
            'explanation': 'The closure encapsulates a dictionary `cache`. When args are seen, the cached value is returned directly, avoiding exponential re-computations.',
            'starter_code': 'def memoize(func):\n    # Implement caching decorator:\n    pass\n\n@memoize\ndef fib(n):\n    if n < 2: return n\n    return fib(n - 1) + fib(n - 2)\n\nprint([fib(i) for i in range(10)])',
            'solution_code': 'def memoize(func):\n    cache = {}\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = func(*args)\n        return cache[args]\n    return wrapper\n\n@memoize\ndef fib(n):\n    if n < 2: return n\n    return fib(n - 1) + fib(n - 2)\n\nprint([fib(i) for i in range(10)])',
            'test_cases': [
                {'input_data': '', 'expected_output': '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]', 'is_sample': True, 'order': 1},
            ]
        },
        {
            'category': cat_data,
            'title': 'Flatten Nested List Structure',
            'slug': 'flatten-nested-list',
            'difficulty': 'hard',
            'points': 30,
            'order': 12,
            'description': 'Write a recursive function or generator `flatten(nested_list)` that flattens arbitrarily nested lists of integers into a single flat list.\n\nInput: `[1, [2, [3, 4], 5], [6, [7, [8, 9]]]]`\nExpected output: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`',
            'example_input': '[1, [2, [3, 4], 5], [6, [7, [8, 9]]]]',
            'example_output': '[1, 2, 3, 4, 5, 6, 7, 8, 9]',
            'hints': 'Check `if isinstance(item, list)`: if so, recursively flatten; otherwise append.',
            'explanation': 'Depth-first recursion traverses nested arrays and appends primitive elements into the accumulator list.',
            'starter_code': 'def flatten(nested):\n    # Flatten arbitrarily nested lists:\n    pass\n\ndata = [1, [2, [3, 4], 5], [6, [7, [8, 9]]]]\nprint(flatten(data))',
            'solution_code': 'def flatten(nested):\n    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result\n\ndata = [1, [2, [3, 4], 5], [6, [7, [8, 9]]]]\nprint(flatten(data))',
            'test_cases': [
                {'input_data': '', 'expected_output': '[1, 2, 3, 4, 5, 6, 7, 8, 9]', 'is_sample': True, 'order': 1},
            ]
        }
    ]

    for ex_data in exercises_data:
        test_cases = ex_data.pop('test_cases')
        exercise, _ = Exercise.objects.update_or_create(
            slug=ex_data['slug'],
            defaults=ex_data
        )

        for tc in test_cases:
            ExerciseTestCase.objects.update_or_create(
                exercise=exercise,
                order=tc['order'],
                defaults={
                    'input_data': tc.get('input_data', ''),
                    'expected_output': tc.get('expected_output', ''),
                    'is_sample': tc.get('is_sample', True)
                }
            )

    print("Exercises & test cases seeded successfully.")
