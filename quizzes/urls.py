from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list_view, name='quiz_list'),
    path('generate/', views.quiz_generator_view, name='quiz_generate'),
    path('dashboard/', views.quiz_dashboard_view, name='quiz_dashboard'),
    path('<slug:slug>/', views.quiz_take_view, name='quiz_take'),
    path('<slug:slug>/submit/', views.quiz_submit_api, name='quiz_submit'),
    path('<slug:slug>/result/<int:attempt_id>/', views.quiz_result_view, name='quiz_result'),
]
