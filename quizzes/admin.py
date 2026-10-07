from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_text', 'question_type', 'category', 'difficulty', 'marks', 'is_active', 'quiz')
    list_filter = ('question_type', 'category', 'difficulty', 'is_active', 'quiz')
    search_fields = ('question_text', 'explanation', 'code_snippet')
    inlines = [QuizOptionInline]
    ordering = ('quiz', 'order', 'id')

class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 0
    fields = ('order', 'question_type', 'category', 'difficulty', 'question_text', 'code_snippet', 'fill_blank_answer', 'marks', 'is_active')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'time_limit_mins', 'pass_percentage', 'is_dynamic', 'is_published')
    list_filter = ('difficulty', 'category', 'is_dynamic', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_marks', 'percentage', 'grade', 'passed', 'completed_at')
    list_filter = ('passed', 'quiz')
    search_fields = ('user__username', 'quiz__title')

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'is_skipped', 'marks_earned')
    list_filter = ('is_correct', 'is_skipped')
