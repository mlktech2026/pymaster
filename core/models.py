from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PageView(models.Model):
    path = models.CharField(max_length=255, db_index=True)
    page_title = models.CharField(max_length=200, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='page_views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, default='')
    referer = models.CharField(max_length=300, blank=True, default='')
    session_key = models.CharField(max_length=50, blank=True, default='')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'

    def __str__(self):
        user_str = self.user.username if self.user else 'Guest'
        return f"{self.path} by {user_str} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
