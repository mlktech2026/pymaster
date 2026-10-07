"""
URL configuration for Python Learning Website.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views
from accounts import views as accounts_views
from tutorials import views as tutorials_views
from exercises import views as exercises_views
from quizzes import views as quizzes_views
from progress import views as progress_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core & SEO pages
    path('', core_views.home_view, name='home'),
    path('roadmap/', core_views.roadmap_view, name='roadmap'),
    path('search/', core_views.search_view, name='search'),
    path('robots.txt', core_views.robots_txt_view, name='robots_txt'),

    # Direct auth shortcuts
    path('login/', accounts_views.login_view, name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('profile/', accounts_views.profile_view, name='profile'),
    path('dashboard/', progress_views.dashboard_view, name='dashboard'),

    # App packages
    path('accounts/', include('accounts.urls')),
    path('tutorials/', include('tutorials.urls')),
    path('exercises/', include('exercises.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('practice/', include('practice.urls')),
    path('projects/', include('projects.urls')),
    path('progress/', include('progress.urls')),

    # SEO URLs matching prompt specifications
    # /python/tutorial/<slug>/
    path('python/tutorial/<slug:slug>/', tutorials_views.tutorial_detail_view, name='tutorial_seo_detail'),
    # /python/exercises/<slug>/
    path('python/exercises/<slug:slug>/', exercises_views.exercise_detail_view, name='exercise_seo_detail'),
    # /python/quizzes/<slug>/
    path('python/quizzes/<slug:slug>/', quizzes_views.quiz_take_view, name='quiz_seo_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
