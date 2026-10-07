from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    description = models.TextField()
    requirements = models.TextField(help_text='List of requirements/prerequisites (one per line or markdown)')
    concepts_used = models.CharField(max_length=300, help_text='Comma separated concepts, e.g. OOP, File I/O, Requests')
    step_by_step_guide = models.TextField(help_text='Detailed implementation tutorial in Markdown')
    source_code = models.TextField(help_text='Complete production-grade runnable source code')
    challenges = models.TextField(blank=True, default='', help_text='Take-it-further exercises and challenges')
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['level', 'order', 'title']

    def __str__(self):
        return f"[{self.get_level_display()}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def concepts_list(self):
        return [c.strip() for c in self.concepts_used.split(',') if c.strip()]
