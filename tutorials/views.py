from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import F, Q
from .models import TutorialCategory, Tutorial, TutorialProgress, VideoTutorial

def tutorial_list_view(request):
    categories = TutorialCategory.objects.prefetch_related('tutorials').all()
    beginner_cats = categories.filter(level='beginner')
    intermediate_cats = categories.filter(level='intermediate')
    advanced_cats = categories.filter(level='advanced')
    
    completed_ids = set()
    if request.user.is_authenticated:
        completed_ids = set(
            TutorialProgress.objects.filter(user=request.user, completed=True)
            .values_list('tutorial_id', flat=True)
        )

    context = {
        'beginner_cats': beginner_cats,
        'intermediate_cats': intermediate_cats,
        'advanced_cats': advanced_cats,
        'completed_ids': completed_ids,
        'total_tutorials': Tutorial.objects.filter(is_published=True).count(),
        'completed_count': len(completed_ids),
    }
    return render(request, 'tutorials/tutorial_list.html', context)

def tutorial_detail_view(request, slug):
    tutorial = get_object_or_404(Tutorial, slug=slug, is_published=True)
    all_categories = TutorialCategory.objects.prefetch_related('tutorials').all()
    
    # Track progress and last visited for authenticated user
    is_completed = False
    completed_ids = set()
    if request.user.is_authenticated:
        progress, _ = TutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial
        )
        progress.last_visited_at = timezone.now()
        progress.save(update_fields=['last_visited_at'])
        is_completed = progress.completed
        
        completed_ids = set(
            TutorialProgress.objects.filter(user=request.user, completed=True)
            .values_list('tutorial_id', flat=True)
        )
        request.user.profile.update_streak()

    # Find previous and next tutorials across the course sequence
    all_tutorials = list(Tutorial.objects.filter(is_published=True).select_related('category').order_by('category__order', 'order', 'id'))
    current_index = -1
    for idx, tut in enumerate(all_tutorials):
        if tut.id == tutorial.id:
            current_index = idx
            break

    prev_tutorial = all_tutorials[current_index - 1] if current_index > 0 else None
    next_tutorial = all_tutorials[current_index + 1] if current_index < len(all_tutorials) - 1 else None

    context = {
        'tutorial': tutorial,
        'all_categories': all_categories,
        'completed_ids': completed_ids,
        'is_completed': is_completed,
        'prev_tutorial': prev_tutorial,
        'next_tutorial': next_tutorial,
    }
    return render(request, 'tutorials/tutorial_detail.html', context)

@login_required
@require_POST
def mark_tutorial_complete(request, slug):
    tutorial = get_object_or_404(Tutorial, slug=slug)
    progress, created = TutorialProgress.objects.get_or_create(
        user=request.user,
        tutorial=tutorial
    )
    
    first_time = not progress.completed
    if first_time:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Award 20 XP
        request.user.profile.add_xp(20)
        request.user.profile.update_streak()
        
        from progress.gamification import check_and_award_badges
        new_badges = check_and_award_badges(request.user)
        
        return JsonResponse({
            'success': True,
            'completed': True,
            'xp_earned': 20,
            'new_badges': [b.name for b in new_badges],
            'message': 'Lesson marked as complete! +20 XP'
        })
    else:
        # Toggle back if desired, or keep as completed
        progress.completed = False
        progress.save()
        return JsonResponse({
            'success': True,
            'completed': False,
            'xp_earned': 0,
            'new_badges': [],
            'message': 'Lesson marked as incomplete'
        })


def video_tutorial_list_view(request):
    """
    Renders video tutorials catalog with search, category filtering, and statistics.
    """
    categories = TutorialCategory.objects.all()
    videos = VideoTutorial.objects.filter(is_published=True).select_related('category')

    # Filter by category
    selected_category = request.GET.get('category')
    if selected_category:
        videos = videos.filter(category__slug=selected_category)

    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        videos = videos.filter(Q(title__icontains=q) | Q(description__icontains=q))

    context = {
        'videos': videos,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': q,
        'total_videos': VideoTutorial.objects.filter(is_published=True).count(),
    }
    return render(request, 'tutorials/video_list.html', context)


def video_tutorial_detail_view(request, slug):
    """
    Renders video tutorial player with HTML5/Embed streaming, view counting, and related videos.
    """
    video = get_object_or_404(VideoTutorial, slug=slug, is_published=True)

    # Increment view counter atomically
    VideoTutorial.objects.filter(pk=video.pk).update(views_count=F('views_count') + 1)
    video.refresh_from_db(fields=['views_count'])

    # Update streak for logged in user
    if request.user.is_authenticated:
        request.user.profile.update_streak()

    # Related videos in same category or recent
    related_videos = VideoTutorial.objects.filter(is_published=True).exclude(pk=video.pk)
    if video.category:
        cat_videos = related_videos.filter(category=video.category)[:4]
        if cat_videos.exists():
            related_videos = cat_videos
        else:
            related_videos = related_videos[:4]
    else:
        related_videos = related_videos[:4]

    all_categories = TutorialCategory.objects.all()

    context = {
        'video': video,
        'related_videos': related_videos,
        'all_categories': all_categories,
    }
    return render(request, 'tutorials/video_detail.html', context)


@login_required
@require_POST
def mark_video_complete(request, slug):
    """
    Awards +30 XP to user upon watching video tutorial.
    """
    video = get_object_or_404(VideoTutorial, slug=slug)
    user = request.user
    user.profile.add_xp(30)
    user.profile.update_streak()

    from progress.gamification import check_and_award_badges
    new_badges = check_and_award_badges(user)

    return JsonResponse({
        'success': True,
        'xp_earned': 30,
        'new_badges': [b.name for b in new_badges],
        'message': f"Great job watching '{video.title}'! +30 XP awarded."
    })

