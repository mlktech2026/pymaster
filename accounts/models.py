from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    total_xp = models.PositiveIntegerField(default=0)
    preferred_theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def update_streak(self):
        today = timezone.now().date()
        if self.last_active_date == today:
            return self.current_streak
        
        if self.last_active_date == today - timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
            
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
            
        self.last_active_date = today
        self.save(update_fields=['current_streak', 'longest_streak', 'last_active_date'])
        
        # Check streak badge
        from progress.gamification import check_and_award_badges
        check_and_award_badges(self.user)
        return self.current_streak

    def add_xp(self, amount):
        if amount > 0:
            self.total_xp += amount
            self.save(update_fields=['total_xp'])

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
