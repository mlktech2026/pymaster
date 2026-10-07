from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_list_view, name='tutorial_list'),
    path('<slug:slug>/', views.tutorial_detail_view, name='tutorial_detail'),
    path('<slug:slug>/complete/', views.mark_tutorial_complete, name='mark_tutorial_complete'),
]
