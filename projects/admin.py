from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'concepts_used', 'order')
    list_filter = ('level',)
    search_fields = ('title', 'description', 'concepts_used')
    prepopulated_fields = {'slug': ('title',)}
