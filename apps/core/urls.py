from django.urls import path
from apps.core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('health/', views.health_check, name='health_check'),
]
