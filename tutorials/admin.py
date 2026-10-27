from django.contrib import admin
from django.utils.html import format_html
from .models import TutorialCategory, Tutorial, TutorialProgress, VideoTutorial

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

@admin.register(VideoTutorial)
class VideoTutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'video_type_badge', 'duration_mins', 'views_count', 'is_published', 'created_at')
    list_editable = ('is_published', 'duration_mins')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description', 'order', 'is_published')
        }),
        ('Video Content & Media Upload', {
            'description': 'Upload a local video file (MP4/WebM) or provide an external video link (YouTube, Vimeo).',
            'fields': ('video_file', 'video_url', 'thumbnail', 'duration_mins')
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',),
        })
    )

    def video_type_badge(self, obj):
        if obj.video_file:
            return format_html('<span style="color:#10b981; font-weight:bold;">📁 File Upload</span>')
        elif obj.video_url:
            return format_html('<span style="color:#3b82f6; font-weight:bold;">🌐 External Link</span>')
        return format_html('<span style="color:#ef4444;">No Video</span>')
    video_type_badge.short_description = 'Media Type'

