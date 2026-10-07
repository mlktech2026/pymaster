from django.contrib import admin
from .models import ExerciseCategory, Exercise, ExerciseTestCase, ExerciseSubmission

class ExerciseTestCaseInline(admin.TabularInline):
    model = ExerciseTestCase
    extra = 1

@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'points', 'order')
    list_filter = ('difficulty', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExerciseTestCaseInline]

@admin.register(ExerciseSubmission)
class ExerciseSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'passed', 'score', 'test_cases_passed', 'total_test_cases', 'created_at')
    list_filter = ('passed', 'created_at')
    search_fields = ('user__username', 'exercise__title')
