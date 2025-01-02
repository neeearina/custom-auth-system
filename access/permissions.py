"""
Custom permission classes for access control.
Кастомные классы разрешений для контроля доступа.
"""
from rest_framework import permissions
from .models import Permission, UserRole


class HasResourcePermission(permissions.BasePermission):
    """
    Custom permission class that checks if user has permission
    to perform an action on a resource.
    Кастомный класс разрешений, который проверяет наличие у пользователя права
    на выполнение действия над ресурсом.
    """
    resource_name = None
    action_name = None
    
    def has_permission(self, request, view):
        """
        Check if user has permission to access the resource.
        Gets resource_name and action_name from the permission class attributes
        or from view attributes.
        Проверка наличия у пользователя права доступа к ресурсу.
        Получает resource_name и action_name из атрибутов класса разрешений
        или из атрибутов представления.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        resource_name = self.resource_name or getattr(view, 'resource_name', None)
        action_name = self.action_name or getattr(view, 'action_name', None)
        
        if not resource_name or not action_name:
            return False
        
        user_roles = UserRole.objects.filter(
            user=request.user,
            role__permissions__resource__name=resource_name,
            role__permissions__action__name=action_name
        ).exists()
        
        return user_roles


def check_user_permission(user, resource_name, action_name):
    """
    Utility function to check if user has permission.
    Утилитная функция для проверки наличия у пользователя права.
    
    Args:
        user: User instance / Экземпляр пользователя
        resource_name: Name of the resource / Имя ресурса
        action_name: Name of the action / Имя действия
    
    Returns:
        bool: True if user has permission, False otherwise
        True если у пользователя есть право, False в противном случае
    """
    if not user or not user.is_authenticated:
        return False
    
    return UserRole.objects.filter(
        user=user,
        role__permissions__resource__name=resource_name,
        role__permissions__action__name=action_name
    ).exists()
