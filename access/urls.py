"""
URL-маршруты для приложения access.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'access'

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'resources', views.ResourceViewSet, basename='resource')
router.register(r'actions', views.ActionViewSet, basename='action')
router.register(r'permissions', views.PermissionViewSet, basename='permission')
router.register(r'user-roles', views.UserRoleViewSet, basename='user-role')

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', views.access_overview, name='overview'),
]
