from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from tutorials.models import Tutorial, TutorialProgress
from exercises.models import Exercise, ExerciseSubmission
from quizzes.models import QuizAttempt
from .models import Badge, UserBadge
from .gamification import ensure_badges_exist

@login_required
def dashboard_view(request):
    user = request.user
    ensure_badges_exist()

    # Total tutorials & completed tutorials
    total_tutorials = Tutorial.objects.filter(is_published=True).count()
    completed_tutorials = TutorialProgress.objects.filter(user=user, completed=True).count()
    course_progress_pct = round((completed_tutorials / total_tutorials * 100), 1) if total_tutorials > 0 else 0

    # Total exercises & solved exercises
    total_exercises = Exercise.objects.count()
    solved_exercises_count = ExerciseSubmission.objects.filter(
        user=user, passed=True
    ).values('exercise_id').distinct().count()

    # Quizzes stats
    quiz_attempts = QuizAttempt.objects.filter(user=user)
    quizzes_completed = quiz_attempts.count()
    avg_quiz_score = quiz_attempts.aggregate(Avg('percentage'))['percentage__avg']
    avg_quiz_score = round(avg_quiz_score, 1) if avg_quiz_score is not None else 0.0

    # Continue Learning - find last visited tutorial
    last_visited_progress = TutorialProgress.objects.filter(
        user=user
    ).order_by('-last_visited_at').select_related('tutorial', 'tutorial__category').first()
    
    last_tutorial = last_visited_progress.tutorial if last_visited_progress else Tutorial.objects.filter(is_published=True).first()

    # Badges
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    earned_badge_ids = set(user_badges.values_list('badge_id', flat=True))
    all_badges = Badge.objects.all()

    # Recent submissions
    recent_submissions = ExerciseSubmission.objects.filter(
        user=user
    ).select_related('exercise').order_by('-created_at')[:5]

    # Recent quiz attempts
    recent_quizzes = QuizAttempt.objects.filter(
        user=user
    ).select_related('quiz').order_by('-completed_at')[:5]

    # Approximate learning time (e.g. tutorials read * 6 mins + exercises solved * 10 mins + quizzes * 5 mins)
    approx_time_mins = (completed_tutorials * 6) + (solved_exercises_count * 10) + (quizzes_completed * 8)
    hours = approx_time_mins // 60
    mins = approx_time_mins % 60
    total_learning_time_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    context = {
        'course_progress_pct': course_progress_pct,
        'completed_tutorials': completed_tutorials,
        'total_tutorials': total_tutorials,
        'solved_exercises_count': solved_exercises_count,
        'total_exercises': total_exercises,
        'quizzes_completed': quizzes_completed,
        'avg_quiz_score': avg_quiz_score,
        'current_streak': user.profile.current_streak,
        'longest_streak': user.profile.longest_streak,
        'total_xp': user.profile.total_xp,
        'total_learning_time_str': total_learning_time_str,
        'last_tutorial': last_tutorial,
        'user_badges': user_badges,
        'all_badges': all_badges,
        'earned_badge_ids': earned_badge_ids,
        'recent_submissions': recent_submissions,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'progress/dashboard.html', context)
