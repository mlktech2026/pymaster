from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('mixed', 'Mixed Levels'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=100, default='Python Basics')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    description = models.TextField(blank=True, default='')
    time_limit_mins = models.PositiveIntegerField(default=10, help_text='Time limit in minutes (0 for no limit)')
    pass_percentage = models.PositiveIntegerField(default=70, help_text='Percentage needed to pass')
    is_published = models.BooleanField(default=True)
    is_dynamic = models.BooleanField(default=False, help_text='Generated dynamically via Quiz Generator')
    total_questions_count = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def total_marks(self):
        return sum(q.marks for q in self.questions.filter(is_active=True))


class QuizQuestion(models.Model):
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Question (MCQ)'),
        ('multiple_select', 'Multiple Select (Checkbox)'),
        ('true_false', 'True / False'),
        ('fill_blank', 'Fill in the Blank'),
        ('code_output', 'Code Output Prediction'),
        ('find_error', 'Find the Error'),
        ('debug_code', 'Debug the Code'),
        ('arrange_code', 'Arrange the Code (Drag & Drop)'),
        ('match_following', 'Match the Following Concepts'),
        ('drag_drop_blank', 'Drag and Drop Answer'),
        ('code_completion', 'Code Completion'),
        ('scenario_based', 'Scenario Based Question'),
        ('order_sequence', 'Order / Sequence Steps'),
        ('identify_output', 'Identify Complex Output'),
        ('predict_variable', 'Predict Variable Value'),
        ('code_ordering', 'Code Ordering'),
        ('diagram_question', 'Image / Diagram Based Question'),
        ('short_answer', 'Short Answer'),
        ('code_comparison', 'Code Comparison'),
        ('mini_challenge', 'Mini Coding Challenge'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='mcq')
    category = models.CharField(max_length=100, default='Python Basics')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    question_text = models.TextField()
    code_snippet = models.TextField(blank=True, default='', help_text='Optional Python code snippet or starter code')
    fill_blank_answer = models.CharField(max_length=255, blank=True, default='', help_text='Accepted answer for text questions')
    
    # JSON field for complex question structures (matching pairs, drag tokens, code blocks, test cases, diagram data)
    question_data = models.JSONField(
        default=dict, 
        blank=True, 
        help_text='JSON structured data for matching pairs, code blocks, test cases, etc.'
    )
    
    explanation = models.TextField(blank=True, default='', help_text='Explanation displayed in answer review')
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"[{self.get_question_type_display()}] Q{self.order}: {self.question_text[:40]}..."


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=400)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        mark = "✓" if self.is_correct else "✗"
        return f"{self.option_text} ({mark})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0.0)
    total_marks = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        status = "PASSED" if self.passed else "FAILED"
        return f"{self.user.username} - {self.quiz.title} ({self.percentage}% - {status})"

    @property
    def grade(self):
        if self.percentage >= 90: return 'A+'
        if self.percentage >= 80: return 'A'
        if self.percentage >= 70: return 'B'
        if self.percentage >= 60: return 'C'
        if self.percentage >= 50: return 'D'
        return 'F'


class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.CharField(max_length=500, blank=True, default='')
    user_answer_json = models.JSONField(default=dict, blank=True)
    is_correct = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    marks_earned = models.FloatField(default=0.0)

    def __str__(self):
        return f"Answer for Q{self.question.order}: {'Correct' if self.is_correct else ('Skipped' if self.is_skipped else 'Wrong')}"
