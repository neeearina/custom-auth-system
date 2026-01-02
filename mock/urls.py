"""
URLs for mock app.
URL-маршруты для приложения mock.
"""
from django.urls import path
from . import views

app_name = 'mock'

urlpatterns = [
    path('projects/', views.mock_projects, name='mock-projects'),
    path('reports/', views.mock_reports, name='mock-reports'),
]
