from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=50, default='fa-laptop-code')
    description = models.TextField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'Exercise Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    description = models.TextField(help_text='Detailed problem statement in Markdown')
    example_input = models.TextField(blank=True, default='')
    example_output = models.TextField(blank=True, default='')
    starter_code = models.TextField(help_text='Template code provided to learner')
    solution_code = models.TextField(help_text='Reference solution code')
    explanation = models.TextField(blank=True, default='', help_text='Explanation revealed after solving')
    hints = models.TextField(blank=True, default='', help_text='Helpful hints for solving')
    points = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['difficulty', 'order', 'title']

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ExerciseTestCase(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField(blank=True, default='', help_text='Stdin input or argument')
    expected_output = models.TextField(help_text='Exact expected stdout output')
    is_sample = models.BooleanField(default=True, help_text='Whether this test case is visible in problem description')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        visible = "Sample" if self.is_sample else "Hidden"
        return f"{self.exercise.title} - TestCase #{self.order} ({visible})"

class ExerciseSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_submissions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    submitted_code = models.TextField()
    passed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    test_cases_passed = models.PositiveIntegerField(default=0)
    total_test_cases = models.PositiveIntegerField(default=0)
    execution_time = models.FloatField(default=0.0)
    output_log = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "PASSED" if self.passed else "FAILED"
        return f"{self.user.username} - {self.exercise.title} ({status})"
