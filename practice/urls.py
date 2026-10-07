from django.urls import path
from . import views

urlpatterns = [
    path('', views.practice_view, name='practice'),
    path('run/', views.run_code_api, name='practice_run_code'),
]
