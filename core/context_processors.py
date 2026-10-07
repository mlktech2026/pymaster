from tutorials.models import Tutorial
from exercises.models import Exercise
from quizzes.models import Quiz

def global_context(request):
    """Provides site-wide context variables to all templates."""
    theme = 'dark'
    user_streak = 0
    user_xp = 0
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        theme = request.user.profile.preferred_theme
        user_streak = request.user.profile.current_streak
        user_xp = request.user.profile.total_xp

    return {
        'SITE_NAME': 'PyMaster',
        'SITE_TAGLINE': 'Learn Python step by step with tutorials, coding exercises, quizzes, and hands-on practice.',
        'user_theme': theme,
        'user_streak': user_streak,
        'user_xp': user_xp,
    }
