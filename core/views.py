import json
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone

from tutorials.models import Tutorial, TutorialCategory, TutorialProgress, VideoTutorial
from exercises.models import Exercise, ExerciseCategory, ExerciseSubmission
from quizzes.models import Quiz
from projects.models import Project
from progress.models import Badge
from .models import PageView

def home_view(request):
    categories = TutorialCategory.objects.prefetch_related('tutorials').all()
    beginner_cats = categories.filter(level='beginner')
    intermediate_cats = categories.filter(level='intermediate')
    advanced_cats = categories.filter(level='advanced')

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
        'beginner_cats': beginner_cats,
        'intermediate_cats': intermediate_cats,
        'advanced_cats': advanced_cats,
        'total_categories_count': categories.count(),
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
        "Disallow: /admin-panel/",
        "Disallow: /practice/run/",
        "Allow: /",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")



@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard_view(request):
    """
    State-of-the-art Admin Analytics & Video Tutorial Management Dashboard.
    Visualizes website users, page views trend graphs, top visited lessons, and video tutorials.
    """
    today = timezone.now().date()

    # 1. High-Level KPI Summary Metrics
    total_users_count = User.objects.count()
    active_learners_count = User.objects.filter(is_staff=False).count()
    staff_count = User.objects.filter(is_staff=True).count()
    
    total_page_views = PageView.objects.count()
    today_page_views = PageView.objects.filter(timestamp__date=today).count()
    
    total_videos_count = VideoTutorial.objects.count()
    total_video_views = VideoTutorial.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
    
    total_exercises_solved = ExerciseSubmission.objects.filter(passed=True).count()
    total_tutorials_completed = TutorialProgress.objects.filter(completed=True).count()

    # 2. Daily Time-Series Data for Graphs (Last 14 Days)
    days_range = 14
    start_date = today - timedelta(days=days_range - 1)

    chart_dates = []
    chart_page_views = []
    chart_unique_visitors = []
    chart_user_signups = []

    for i in range(days_range):
        curr_date = start_date + timedelta(days=i)
        chart_dates.append(curr_date.strftime('%b %d'))

        # Views on this day
        day_views_qs = PageView.objects.filter(timestamp__date=curr_date)
        day_views_count = day_views_qs.count()
        day_unique_count = day_views_qs.values('ip_address').distinct().count()

        chart_page_views.append(day_views_count)
        chart_unique_visitors.append(day_unique_count)

        # New user signups on this day
        new_users_count = User.objects.filter(date_joined__date=curr_date).count()
        chart_user_signups.append(new_users_count)

    # 3. Top Most Visited Pages & Tutorials
    top_pages_qs = (
        PageView.objects.values('path')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )
    top_pages_labels = [p['path'] for p in top_pages_qs]
    top_pages_counts = [p['total'] for p in top_pages_qs]

    # 4. Video Tutorial Distribution & Views by Category
    categories = TutorialCategory.objects.all()
    cat_video_labels = []
    cat_video_views = []
    for cat in categories:
        c_views = VideoTutorial.objects.filter(category=cat).aggregate(Sum('views_count'))['views_count__sum'] or 0
        if c_views > 0 or VideoTutorial.objects.filter(category=cat).exists():
            cat_video_labels.append(cat.name)
            cat_video_views.append(c_views)

    # 5. All Uploaded Video Tutorials
    video_tutorials = VideoTutorial.objects.select_related('category').order_by('-created_at')

    # 6. Website Users List (Recent 25)
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:25]

    # 7. Live Recent Page Views Feed (Recent 15)
    recent_page_views = PageView.objects.select_related('user').order_by('-timestamp')[:15]

    context = {
        # KPIs
        'total_users_count': total_users_count,
        'active_learners_count': active_learners_count,
        'staff_count': staff_count,
        'total_page_views': total_page_views,
        'today_page_views': today_page_views,
        'total_videos_count': total_videos_count,
        'total_video_views': total_video_views,
        'total_exercises_solved': total_exercises_solved,
        'total_tutorials_completed': total_tutorials_completed,

        # Chart JSON data
        'chart_dates_json': json.dumps(chart_dates),
        'chart_page_views_json': json.dumps(chart_page_views),
        'chart_unique_visitors_json': json.dumps(chart_unique_visitors),
        'chart_user_signups_json': json.dumps(chart_user_signups),
        'top_pages_labels_json': json.dumps(top_pages_labels),
        'top_pages_counts_json': json.dumps(top_pages_counts),
        'cat_video_labels_json': json.dumps(cat_video_labels),
        'cat_video_views_json': json.dumps(cat_video_views),

        # Management collections
        'video_tutorials': video_tutorials,
        'categories': categories,
        'recent_users': recent_users,
        'recent_page_views': recent_page_views,
    }
    return render(request, 'core/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_upload_video_view(request):
    """
    Handles uploading tutorial videos with title, description, video file/URL, and thumbnail.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        video_file = request.FILES.get('video_file')
        video_url = request.POST.get('video_url', '').strip()
        thumbnail = request.FILES.get('thumbnail')
        duration_mins = request.POST.get('duration_mins', 10)
        is_published = request.POST.get('is_published') == 'on'
        order = request.POST.get('order', 1)

        if not title:
            messages.error(request, "Video title is required.")
            return redirect('admin_panel')

        if not video_file and not video_url:
            messages.error(request, "Please either upload a video file or provide an external video URL.")
            return redirect('admin_panel')

        category = None
        if category_id:
            category = TutorialCategory.objects.filter(id=category_id).first()

        try:
            duration_val = max(1, int(duration_mins))
        except (ValueError, TypeError):
            duration_val = 10

        try:
            order_val = int(order)
        except (ValueError, TypeError):
            order_val = 1

        video = VideoTutorial(
            title=title,
            description=description,
            category=category,
            video_url=video_url,
            duration_mins=duration_val,
            order=order_val,
            is_published=is_published,
        )

        if video_file:
            video.video_file = video_file
        if thumbnail:
            video.thumbnail = thumbnail

        video.save()
        messages.success(request, f"Video Tutorial '{video.title}' uploaded and published successfully!")
        return redirect('admin_panel')

    return redirect('admin_panel')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@require_POST
def admin_delete_video_view(request, pk):
    """
    Deletes a video tutorial from the admin panel.
    """
    video = get_object_or_404(VideoTutorial, pk=pk)
    title = video.title
    video.delete()
    messages.success(request, f"Video Tutorial '{title}' has been deleted.")
    return redirect('admin_panel')

