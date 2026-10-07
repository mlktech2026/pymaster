from django.contrib import admin
from .models import TutorialCategory, Tutorial, TutorialProgress

@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order', 'slug')
    list_editable = ('order',)
    list_filter = ('level',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'estimated_read_time', 'is_published')
    list_editable = ('order', 'is_published')
    list_filter = ('category__level', 'category', 'is_published')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(TutorialProgress)
class TutorialProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutorial', 'completed', 'completed_at', 'last_visited_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('user__username', 'tutorial__title')
