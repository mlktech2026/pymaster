import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from quizzes.models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer
from quizzes.validators import validate_question_answer


class QuestionValidationTests(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Validation Test Quiz", slug="val-quiz", pass_percentage=70)

    def test_mcq_and_variants(self):
        # Covers mcq, code_output, find_error, scenario_based, identify_output, diagram_question, code_comparison
        types_to_test = ['mcq', 'code_output', 'find_error', 'scenario_based', 'identify_output', 'diagram_question', 'code_comparison']
        for qt in types_to_test:
            q = QuizQuestion.objects.create(quiz=self.quiz, question_type=qt, question_text=f"Test {qt}", marks=1)
            o_wrong = QuizOption.objects.create(question=q, option_text="False Choice", is_correct=False, order=1)
            o_right = QuizOption.objects.create(question=q, option_text="True Choice", is_correct=True, order=2)

            # Correct ID
            r1 = validate_question_answer(q, o_right.id)
            self.assertTrue(r1['is_correct'], f"Failed on {qt} correct")
            self.assertEqual(r1['marks_earned'], 1.0)

            # Wrong ID
            r2 = validate_question_answer(q, o_wrong.id)
            self.assertFalse(r2['is_correct'], f"Failed on {qt} wrong")
            self.assertEqual(r2['marks_earned'], 0.0)

            # Skipped
            r3 = validate_question_answer(q, "")
            self.assertTrue(r3['is_skipped'], f"Failed on {qt} skipped")

    def test_true_false(self):
        q = QuizQuestion.objects.create(quiz=self.quiz, question_type='true_false', question_text="Is Python dynamic?", marks=1)
        QuizOption.objects.create(question=q, option_text="True", is_correct=True, order=1)
        QuizOption.objects.create(question=q, option_text="False", is_correct=False, order=2)

        # Match by text
        r_text = validate_question_answer(q, "true")
        self.assertTrue(r_text['is_correct'])

        r_wrong = validate_question_answer(q, "false")
        self.assertFalse(r_wrong['is_correct'])

    def test_multiple_select(self):
        q = QuizQuestion.objects.create(quiz=self.quiz, question_type='multiple_select', question_text="Select mutable types", marks=2)
        o1 = QuizOption.objects.create(question=q, option_text="list", is_correct=True, order=1)
        o2 = QuizOption.objects.create(question=q, option_text="dict", is_correct=True, order=2)
        o3 = QuizOption.objects.create(question=q, option_text="tuple", is_correct=False, order=3)

        # Correct multi selection
        r_corr = validate_question_answer(q, [o1.id, o2.id])
        self.assertTrue(r_corr['is_correct'])
        self.assertEqual(r_corr['marks_earned'], 2.0)

        # Missing one
        r_partial = validate_question_answer(q, [o1.id])
        self.assertFalse(r_partial['is_correct'])

        # Including wrong
        r_wrong = validate_question_answer(q, [o1.id, o2.id, o3.id])
        self.assertFalse(r_wrong['is_correct'])

    def test_text_input_types(self):
        # fill_blank, code_completion, predict_variable, short_answer
        text_types = ['fill_blank', 'code_completion', 'predict_variable', 'short_answer']
        for tt in text_types:
            q = QuizQuestion.objects.create(
                quiz=self.quiz, question_type=tt, question_text=f"Test {tt}",
                fill_blank_answer="def", question_data={'accepted_answers': ['def', 'def ']}, marks=1
            )
            r_ok = validate_question_answer(q, "DEF")
            self.assertTrue(r_ok['is_correct'], f"Failed on {tt}")

            r_bad = validate_question_answer(q, "class")
            self.assertFalse(r_bad['is_correct'], f"Failed on {tt}")

    def test_drag_drop_blank(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='drag_drop_blank', question_text="Drag token",
            fill_blank_answer="in", question_data={'correct_token': 'in'}, marks=1
        )
        r_ok = validate_question_answer(q, "in")
        self.assertTrue(r_ok['is_correct'])
        r_bad = validate_question_answer(q, "not")
        self.assertFalse(r_bad['is_correct'])

    def test_ordering_types(self):
        # arrange_code, code_ordering, order_sequence
        order_types = ['arrange_code', 'code_ordering', 'order_sequence']
        for ot in order_types:
            q = QuizQuestion.objects.create(
                quiz=self.quiz, question_type=ot, question_text=f"Order {ot}",
                marks=2, question_data={'correct_order': ['step 1', 'step 2', 'step 3']}
            )
            r_ok = validate_question_answer(q, ['step 1', 'step 2', 'step 3'])
            self.assertTrue(r_ok['is_correct'], f"Failed on {ot} correct order")

            r_bad = validate_question_answer(q, ['step 2', 'step 1', 'step 3'])
            self.assertFalse(r_bad['is_correct'], f"Failed on {ot} wrong order")

    def test_match_following(self):
        q = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='match_following', question_text="Match datatypes",
            marks=2, question_data={
                'correct_pairs': {'dict': 'Key-Value', 'set': 'Unique values'}
            }
        )
        r_ok = validate_question_answer(q, {'dict': 'Key-Value', 'set': 'Unique values'})
        self.assertTrue(r_ok['is_correct'])

        r_bad = validate_question_answer(q, {'dict': 'Unique values', 'set': 'Key-Value'})
        self.assertFalse(r_bad['is_correct'])

    def test_sandbox_coding_types(self):
        # debug_code
        q_debug = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='debug_code', question_text="Fix greeting",
            marks=3, question_data={'expected_output': 'Hello Python'}
        )
        r_ok = validate_question_answer(q_debug, "print('Hello Python')")
        self.assertTrue(r_ok['is_correct'])

        r_bad = validate_question_answer(q_debug, "print('Hello World')")
        self.assertFalse(r_bad['is_correct'])

        # mini_challenge with test cases
        q_mini = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='mini_challenge', question_text="Square number",
            marks=3, question_data={
                'test_cases': [
                    {'input': '4', 'output': '16'},
                    {'input': '5', 'output': '25'},
                ]
            }
        )
        solution = "n = int(input())\nprint(n * n)"
        r_mini_ok = validate_question_answer(q_mini, solution)
        self.assertTrue(r_mini_ok['is_correct'])


class QuizViewFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='pass1234')

        # Create a sample curated quiz with 3 questions
        self.quiz = Quiz.objects.create(
            title="Curated Test Quiz",
            slug="curated-test-quiz",
            category="Python Basics",
            difficulty="beginner",
            time_limit_mins=10,
            pass_percentage=70,
            is_published=True
        )

        self.q1 = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='mcq', question_text="What is type(5)?", marks=1, order=1
        )
        self.q1_o1 = QuizOption.objects.create(question=self.q1, option_text="<class 'int'>", is_correct=True, order=1)
        self.q1_o2 = QuizOption.objects.create(question=self.q1, option_text="<class 'str'>", is_correct=False, order=2)

        self.q2 = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='fill_blank', question_text="Keyword to output text?",
            fill_blank_answer="print", question_data={'accepted_answers': ['print']}, marks=1, order=2
        )

        self.q3 = QuizQuestion.objects.create(
            quiz=self.quiz, question_type='arrange_code', question_text="Arrange lines",
            question_data={'correct_order': ['x = 1', 'print(x)']}, marks=2, order=3
        )

    def test_quiz_catalog_view(self):
        response = self.client.get('/quizzes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Curated Test Quiz")

    def test_quiz_take_view(self):
        response = self.client.get(f'/quizzes/{self.quiz.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Curated Test Quiz")
        self.assertContains(response, "What is type(5)?")
        self.assertContains(response, "questions-viewport")

    def test_quiz_submit_api_full_flow(self):
        self.client.login(username='student1', password='pass1234')
        submit_payload = {
            'answers': {
                str(self.q1.id): self.q1_o1.id,            # Correct: 1 mark
                str(self.q2.id): "print",                   # Correct: 1 mark
                str(self.q3.id): ['x = 1', 'print(x)']      # Correct: 2 marks
            },
            'time_taken_seconds': 45
        }

        response = self.client.post(
            f'/quizzes/{self.quiz.slug}/submit/',
            data=json.dumps(submit_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['score'], 4.0)
        self.assertEqual(data['percentage'], 100.0)
        self.assertTrue(data['passed'])

        # Verify attempt record in DB
        attempt = QuizAttempt.objects.get(id=data['attempt_id'])
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.score, 4.0)
        self.assertEqual(attempt.passed, True)
        self.assertEqual(attempt.answers.count(), 3)

        # Test viewing the result page
        res_view = self.client.get(f'/quizzes/{self.quiz.slug}/result/{attempt.id}/')
        self.assertEqual(res_view.status_code, 200)
        self.assertContains(res_view, "100.0%")
        self.assertContains(res_view, "Quiz Passed")

    def test_quiz_generator_post_creates_dynamic_quiz(self):
        response = self.client.post('/quizzes/generate/', {
            'category': 'all',
            'difficulty': 'mixed',
            'question_count': 2,
            'time_limit': 5
        })
        # Should redirect to generated quiz slug
        self.assertEqual(response.status_code, 302)
        redirect_url = response.url
        self.assertTrue(redirect_url.startswith('/quizzes/custom-quiz-'))

        # Fetch the dynamically created quiz
        slug = redirect_url.strip('/').split('/')[-1]
        dyn_quiz = Quiz.objects.get(slug=slug)
        self.assertTrue(dyn_quiz.is_dynamic)
        self.assertGreaterEqual(dyn_quiz.questions.count(), 1)

    def test_quiz_dashboard_view(self):
        self.client.login(username='student1', password='pass1234')
        # Create an attempt
        QuizAttempt.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=3.0,
            total_marks=4.0,
            percentage=75.0,
            passed=True,
            time_taken_seconds=60
        )
        response = self.client.get('/quizzes/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz Performance Dashboard")
        self.assertContains(response, "Curated Test Quiz")
        self.assertContains(response, "75.0%")
