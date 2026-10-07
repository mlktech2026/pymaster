from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'total_xp', 'last_active_date', 'preferred_theme')
    search_fields = ('user__username', 'user__email')
    list_filter = ('preferred_theme', 'last_active_date')
