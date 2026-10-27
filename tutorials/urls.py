from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_list_view, name='tutorial_list'),
    path('videos/', views.video_tutorial_list_view, name='video_tutorial_list'),
    path('videos/<slug:slug>/', views.video_tutorial_detail_view, name='video_tutorial_detail'),
    path('videos/<slug:slug>/complete/', views.mark_video_complete, name='mark_video_complete'),
    path('<slug:slug>/', views.tutorial_detail_view, name='tutorial_detail'),
    path('<slug:slug>/complete/', views.mark_tutorial_complete, name='mark_tutorial_complete'),
]

