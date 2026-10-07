from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from tutorials.models import Tutorial, TutorialCategory
from exercises.models import Exercise, ExerciseCategory
from quizzes.models import Quiz
from projects.models import Project
from progress.models import Badge

def home_view(request):
    beginner_tutorials = Tutorial.objects.filter(category__level='beginner', is_published=True)[:6]
    popular_tutorials = Tutorial.objects.filter(is_published=True).order_by('?')[:6]
    featured_exercises = Exercise.objects.select_related('category').all()[:6]
    featured_quizzes = Quiz.objects.filter(is_published=True)[:4]
    badges_preview = Badge.objects.all()[:6]
    featured_projects = Project.objects.all()[:3]

    context = {
        'beginner_tutorials': beginner_tutorials,
        'popular_tutorials': popular_tutorials,
        'featured_exercises': featured_exercises,
        'featured_quizzes': featured_quizzes,
        'badges_preview': badges_preview,
        'featured_projects': featured_projects,
        'total_tutorials_count': Tutorial.objects.filter(is_published=True).count(),
        'total_exercises_count': Exercise.objects.count(),
        'total_quizzes_count': Quiz.objects.filter(is_published=True).count(),
    }
    return render(request, 'core/home.html', context)

def roadmap_view(request):
    categories = TutorialCategory.objects.prefetch_related('tutorials').all()
    beginner_cats = categories.filter(level='beginner')
    intermediate_cats = categories.filter(level='intermediate')
    advanced_cats = categories.filter(level='advanced')

    context = {
        'beginner_cats': beginner_cats,
        'intermediate_cats': intermediate_cats,
        'advanced_cats': advanced_cats,
    }
    return render(request, 'core/roadmap.html', context)

def search_view(request):
    query = request.GET.get('q', '').strip()
    tutorials_results = []
    exercises_results = []
    quizzes_results = []
    projects_results = []

    if query:
        tutorials_results = Tutorial.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).select_related('category')[:15]

        exercises_results = Exercise.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        ).select_related('category')[:15]

        quizzes_results = Quiz.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query) | Q(description__icontains=query),
            is_published=True
        )[:15]

        projects_results = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(concepts_used__icontains=query)
        )[:10]

    total_matches = len(tutorials_results) + len(exercises_results) + len(quizzes_results) + len(projects_results)

    context = {
        'query': query,
        'tutorials_results': tutorials_results,
        'exercises_results': exercises_results,
        'quizzes_results': quizzes_results,
        'projects_results': projects_results,
        'total_matches': total_matches,
    }
    return render(request, 'core/search_results.html', context)

def robots_txt_view(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /practice/run/",
        "Allow: /",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
