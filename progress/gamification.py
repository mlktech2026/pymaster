from django.utils import timezone
from .models import Badge, UserBadge
from tutorials.models import Tutorial, TutorialProgress
from exercises.models import Exercise, ExerciseSubmission
from quizzes.models import QuizAttempt

BADGE_DEFINITIONS = [
    {
        'name': 'Python Beginner',
        'slug': 'python-beginner',
        'description': 'Completed your very first Python lesson.',
        'icon': 'fa-seedling',
        'badge_color': 'emerald',
    },
    {
        'name': 'First Exercise',
        'slug': 'first-exercise',
        'description': 'Successfully solved your first Python coding exercise.',
        'icon': 'fa-code',
        'badge_color': 'blue',
    },
    {
        'name': 'First Quiz',
        'slug': 'first-quiz',
        'description': 'Completed your first knowledge evaluation quiz.',
        'icon': 'fa-circle-question',
        'badge_color': 'indigo',
    },
    {
        'name': '10 Exercises Completed',
        'slug': '10-exercises-completed',
        'description': 'Solved 10 coding exercises successfully.',
        'icon': 'fa-fire',
        'badge_color': 'amber',
    },
    {
        'name': '50 Exercises Completed',
        'slug': '50-exercises-completed',
        'description': 'Solved 50 coding exercises! Master problem solver.',
        'icon': 'fa-trophy',
        'badge_color': 'yellow',
    },
    {
        'name': 'Python Basics Completed',
        'slug': 'python-basics-completed',
        'description': 'Completed all beginner tutorials.',
        'icon': 'fa-graduation-cap',
        'badge_color': 'purple',
    },
    {
        'name': 'Quiz Master',
        'slug': 'quiz-master',
        'description': 'Scored a perfect 100% on any quiz challenge.',
        'icon': 'fa-crown',
        'badge_color': 'rose',
    },
    {
        'name': '7 Day Learning Streak',
        'slug': '7-day-learning-streak',
        'description': 'Maintained a coding streak for 7 consecutive days.',
        'icon': 'fa-bolt',
        'badge_color': 'orange',
    },
]

def ensure_badges_exist():
    """Ensures predefined badges exist in the database."""
    for b_data in BADGE_DEFINITIONS:
        Badge.objects.get_or_create(
            slug=b_data['slug'],
            defaults={
                'name': b_data['name'],
                'description': b_data['description'],
                'icon': b_data['icon'],
                'badge_color': b_data['badge_color']
            }
        )

def check_and_award_badges(user):
    """
    Evaluates eligibility criteria for all badges and awards newly earned ones.
    Returns list of newly awarded Badge objects.
    """
    ensure_badges_exist()
    existing_badge_slugs = set(
        UserBadge.objects.filter(user=user).values_list('badge__slug', flat=True)
    )

    newly_awarded = []

    def award(badge_slug):
        if badge_slug not in existing_badge_slugs:
            badge = Badge.objects.filter(slug=badge_slug).first()
            if badge:
                UserBadge.objects.create(user=user, badge=badge)
                newly_awarded.append(badge)
                existing_badge_slugs.add(badge_slug)

    # 1. Python Beginner: at least 1 tutorial completed
    tutorials_completed = TutorialProgress.objects.filter(user=user, completed=True).count()
    if tutorials_completed >= 1:
        award('python-beginner')

    # 2. First Exercise: at least 1 exercise solved
    solved_exercises_count = ExerciseSubmission.objects.filter(
        user=user, passed=True
    ).values('exercise_id').distinct().count()
    if solved_exercises_count >= 1:
        award('first-exercise')

    # 3. First Quiz: at least 1 quiz completed
    quiz_attempts_count = QuizAttempt.objects.filter(user=user).count()
    if quiz_attempts_count >= 1:
        award('first-quiz')

    # 4. 10 Exercises Completed
    if solved_exercises_count >= 10:
        award('10-exercises-completed')

    # 5. 50 Exercises Completed
    if solved_exercises_count >= 50:
        award('50-exercises-completed')

    # 6. Python Basics Completed: all beginner tutorials done
    beginner_tutorials_count = Tutorial.objects.filter(category__level='beginner', is_published=True).count()
    if beginner_tutorials_count > 0:
        beginner_completed = TutorialProgress.objects.filter(
            user=user,
            completed=True,
            tutorial__category__level='beginner'
        ).count()
        if beginner_completed >= beginner_tutorials_count:
            award('python-basics-completed')

    # 7. Quiz Master: scored 100% on any quiz
    has_perfect_quiz = QuizAttempt.objects.filter(user=user, percentage__gte=100.0).exists()
    if has_perfect_quiz:
        award('quiz-master')

    # 8. 7 Day Learning Streak
    if hasattr(user, 'profile'):
        if user.profile.current_streak >= 7 or user.profile.longest_streak >= 7:
            award('7-day-learning-streak')

    return newly_awarded
