from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercise_list_view, name='exercise_list'),
    path('<slug:slug>/', views.exercise_detail_view, name='exercise_detail'),
    path('<slug:slug>/run/', views.run_sample_tests_api, name='exercise_run_tests'),
    path('<slug:slug>/submit/', views.submit_exercise_api, name='exercise_submit'),
]
