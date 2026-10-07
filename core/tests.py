from django.test import TestCase, Client
from django.contrib.auth.models import User
from practice.sandbox import execute_python_code, sanitize_code
from tutorials.models import Tutorial, TutorialCategory, TutorialProgress
from exercises.models import Exercise, ExerciseCategory, ExerciseTestCase, ExerciseSubmission
from quizzes.models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer
from quizzes.validators import validate_question_answer
from progress.models import Badge, UserBadge
from progress.gamification import check_and_award_badges, ensure_badges_exist

class SandboxSecurityTests(TestCase):
    def test_basic_execution(self):
        res = execute_python_code('print("Hello from Sandbox!")')
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['stdout'].strip(), "Hello from Sandbox!")
        self.assertEqual(res['is_timeout'], False)

    def test_timeout_infinite_loop(self):
        res = execute_python_code('while True: pass', timeout=1)
        self.assertEqual(res['status'], 'timeout')
        self.assertTrue(res['is_timeout'])

    def test_blocked_os_system(self):
        code = 'import os\nos.system("dir")'
        is_safe, error = sanitize_code(code)
        self.assertFalse(is_safe)
        self.assertIn("Security restriction", error)

    def test_blocked_subprocess_module(self):
        code = 'import subprocess'
        is_safe, error = sanitize_code(code)
        self.assertFalse(is_safe)
        self.assertIn("subprocess", error)

    def test_syntax_error_handling(self):
        res = execute_python_code('def bad_syntax(:')
        self.assertEqual(res['status'], 'error')
        self.assertIn('SyntaxError', res['stderr'])


class QuizValidationEngineTests(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Test Quiz", slug="test-quiz")

    def test_mcq_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='mcq', question_text='What is 2+2?', marks=1
        )
        opt_wrong = QuizOption.objects.create(question=q, option_text='3', is_correct=False, order=1)
        opt_right = QuizOption.objects.create(question=q, option_text='4', is_correct=True, order=2)

        # Correct answer
        res1 = validate_question_answer(q, opt_right.id)
        self.assertTrue(res1['is_correct'])
        self.assertEqual(res1['marks_earned'], 1.0)

        # Wrong answer
        res2 = validate_question_answer(q, opt_wrong.id)
        self.assertFalse(res2['is_correct'])
        self.assertEqual(res2['marks_earned'], 0.0)

        # Skipped
        res3 = validate_question_answer(q, "")
        self.assertTrue(res3['is_skipped'])

    def test_multiple_select_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='multiple_select', question_text='Select evens', marks=2
        )
        o1 = QuizOption.objects.create(question=q, option_text='2', is_correct=True, order=1)
        o2 = QuizOption.objects.create(question=q, option_text='3', is_correct=False, order=2)
        o3 = QuizOption.objects.create(question=q, option_text='4', is_correct=True, order=3)

        # All correct selected
        res1 = validate_question_answer(q, [o1.id, o3.id])
        self.assertTrue(res1['is_correct'])
        self.assertEqual(res1['marks_earned'], 2.0)

        # Only one selected
        res2 = validate_question_answer(q, [o1.id])
        self.assertFalse(res2['is_correct'])

    def test_true_false_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='true_false', question_text='Python is interpreted', marks=1
        )
        QuizOption.objects.create(question=q, option_text='True', is_correct=True, order=1)
        QuizOption.objects.create(question=q, option_text='False', is_correct=False, order=2)

        res = validate_question_answer(q, 'True')
        self.assertTrue(res['is_correct'])

    def test_fill_blank_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='fill_blank', question_text='Function keyword',
            fill_blank_answer='def', marks=1, question_data={'accepted_answers': ['def']}
        )
        res = validate_question_answer(q, 'def')
        self.assertTrue(res['is_correct'])

    def test_arrange_code_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='arrange_code', question_text='Arrange code',
            marks=2, question_data={
                'shuffled_blocks': ['b', 'a'],
                'correct_order': ['a', 'b']
            }
        )
        # Correct order
        res1 = validate_question_answer(q, ['a', 'b'])
        self.assertTrue(res1['is_correct'])

        # Incorrect order
        res2 = validate_question_answer(q, ['b', 'a'])
        self.assertFalse(res2['is_correct'])

    def test_match_following_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='match_following', question_text='Match items',
            marks=2, question_data={
                'correct_pairs': {'k1': 'v1', 'k2': 'v2'}
            }
        )
        res1 = validate_question_answer(q, {'k1': 'v1', 'k2': 'v2'})
        self.assertTrue(res1['is_correct'])

        res2 = validate_question_answer(q, {'k1': 'wrong', 'k2': 'v2'})
        self.assertFalse(res2['is_correct'])

    def test_drag_drop_blank_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='drag_drop_blank', question_text='Drag keyword',
            marks=2, question_data={'correct_token': 'for'}
        )
        res = validate_question_answer(q, 'for')
        self.assertTrue(res['is_correct'])

    def test_debug_code_validation(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='debug_code', question_text='Fix output',
            marks=3, question_data={'expected_output': '42'}
        )
        res = validate_question_answer(q, 'print(40 + 2)')
        self.assertTrue(res['is_correct'])


class GamificationAndBadgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        ensure_badges_exist()

    def test_user_profile_creation_and_streak(self):
        self.assertIsNotNone(self.user.profile)
        streak = self.user.profile.update_streak()
        self.assertEqual(streak, 1)

    def test_award_python_beginner_badge(self):
        cat = TutorialCategory.objects.create(name='Basics', slug='basics', level='beginner')
        tut = Tutorial.objects.create(
            category=cat, title='Lesson 1', slug='lesson-1',
            summary='Sum', content='Content'
        )
        TutorialProgress.objects.create(user=self.user, tutorial=tut, completed=True)

        new_badges = check_and_award_badges(self.user)
        badge_slugs = [b.slug for b in new_badges]
        self.assertIn('python-beginner', badge_slugs)


class PlatformViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='gowtham', password='python123')

    def test_homepage_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_quiz_catalog_status(self):
        response = self.client.get('/quizzes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modern Python Quiz System")

    def test_quiz_generator_get(self):
        response = self.client.get('/quizzes/generate/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Random Quiz Generator")

    def test_quiz_dashboard_view(self):
        self.client.login(username='gowtham', password='python123')
        response = self.client.get('/quizzes/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz Performance Dashboard")
