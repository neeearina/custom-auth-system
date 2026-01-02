"""
Admin configuration for access app.
Конфигурация админ-панели для приложения access.
"""
from django.contrib import admin
from .models import Role, Resource, Action, Permission, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    Интерфейс админ-панели для модели Role.
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Admin interface for Resource model.
    Интерфейс админ-панели для модели Resource.
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """
    Admin interface for Action model.
    Интерфейс админ-панели для модели Action.
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin interface for Permission model.
    Интерфейс админ-панели для модели Permission.
    """
    list_display = ('role', 'resource', 'action', 'created_at')
    list_filter = ('role', 'resource', 'action')
    search_fields = ('role__name', 'resource__name', 'action__name')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Admin interface for UserRole model.
    Интерфейс админ-панели для модели UserRole.
    """
    list_display = ('user', 'role', 'assigned_at')
    list_filter = ('role', 'assigned_at')
    search_fields = ('user__email', 'user__full_name', 'role__name')
