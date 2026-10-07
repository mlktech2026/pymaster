from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class TutorialCategory(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner Level'),
        ('intermediate', 'Intermediate Level'),
        ('advanced', 'Advanced Level'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    description = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=60, default='fa-book', help_text='FontAwesome icon class, e.g. fa-code, fa-rocket')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Tutorial Categories'

    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tutorial(models.Model):
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, related_name='tutorials')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    order = models.PositiveIntegerField(default=1)
    summary = models.TextField(help_text='Brief 1-2 sentence overview for cards and meta description')
    
    # Detailed lesson sections matching prompt specification
    content = models.TextField(help_text='Main explanation in Markdown or HTML')
    syntax = models.TextField(blank=True, default='', help_text='Syntax explanation or template')
    code_example = models.TextField(blank=True, default='', help_text='Primary Python code example')
    expected_output = models.TextField(blank=True, default='', help_text='Expected output of code_example')
    important_notes = models.TextField(blank=True, default='', help_text='Important points or gotchas')
    common_mistakes = models.TextField(blank=True, default='', help_text='Common pitfalls and mistakes to avoid')
    real_world_example = models.TextField(blank=True, default='', help_text='Practical industry or real-world use case')
    practice_code = models.TextField(blank=True, default='', help_text='Starter code for Try It Yourself editor')
    
    estimated_read_time = models.PositiveIntegerField(default=5, help_text='Estimated reading time in minutes')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'order', 'id']

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class TutorialProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorial_progress')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_visited_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tutorial')

    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.user.username} - {self.tutorial.title} ({status})"
