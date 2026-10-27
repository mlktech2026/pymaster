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


class VideoTutorial(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    category = models.ForeignKey(
        TutorialCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='video_tutorials'
    )
    description = models.TextField(help_text='Detailed overview and syllabus of what this video tutorial covers')
    video_file = models.FileField(
        upload_to='tutorials/videos/', 
        blank=True, 
        null=True, 
        help_text='Upload tutorial video file (MP4, WebM, OGG, MOV)'
    )
    video_url = models.CharField(
        max_length=500, 
        blank=True, 
        default='', 
        help_text='Optional external video stream (e.g. YouTube, Vimeo, or Cloud CDN URL)'
    )
    thumbnail = models.ImageField(
        upload_to='tutorials/thumbnails/', 
        blank=True, 
        null=True, 
        help_text='Custom preview cover image for the video card'
    )
    duration_mins = models.PositiveIntegerField(default=10, help_text='Duration in minutes')
    views_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Video Tutorial'
        verbose_name_plural = 'Video Tutorials'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'video-tutorial'
            slug = base_slug
            counter = 1
            while VideoTutorial.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def has_video(self):
        return bool(self.video_file or self.video_url)

    @property
    def video_file_url(self):
        if self.video_file:
            try:
                return self.video_file.url
            except ValueError:
                return ''
        return ''

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            try:
                return self.thumbnail.url
            except ValueError:
                return ''
        return ''

    @property
    def embed_url(self):
        """Converts standard YouTube or Vimeo links to responsive embed URLs."""
        if not self.video_url:
            return ''
        url = self.video_url.strip()
        if 'youtube.com/watch' in url:
            try:
                video_id = url.split('v=')[1].split('&')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            except Exception:
                pass
        elif 'youtu.be/' in url:
            try:
                video_id = url.split('youtu.be/')[1].split('?')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            except Exception:
                pass
        elif 'vimeo.com/' in url:
            try:
                video_id = url.split('vimeo.com/')[1].split('?')[0]
                return f"https://player.vimeo.com/video/{video_id}"
            except Exception:
                pass
        return url
