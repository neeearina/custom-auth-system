"""
Views for access app (admin API).
Представления для приложения access (административный API).
"""
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Role, Resource, Action, Permission, UserRole
from .serializers import (
    RoleSerializer,
    ResourceSerializer,
    ActionSerializer,
    PermissionSerializer,
    UserRoleSerializer
)
from .permissions import check_user_permission


class IsAdminPermission(IsAuthenticated):
    """
    Permission class that checks if user has admin role.
    Класс разрешений, который проверяет наличие у пользователя роли admin.
    """
    
    def has_permission(self, request, view):
        """
        Check if user has admin role.
        Проверка наличия у пользователя роли admin.
        """
        if not super().has_permission(request, view):
            return False
        return check_user_permission(request.user, 'access', 'admin')


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing roles (admin only).
    ViewSet для управления ролями (только для админов).
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminPermission]


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing resources (admin only).
    ViewSet для управления ресурсами (только для админов).
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminPermission]


class ActionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing actions (admin only).
    ViewSet для управления действиями (только для админов).
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAdminPermission]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing permissions (admin only).
    ViewSet для управления правами доступа (только для админов).
    """
    queryset = Permission.objects.select_related('role', 'resource', 'action').all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminPermission]
    
    def get_queryset(self):
        """
        Filter permissions by role, resource, or action.
        Фильтрация прав доступа по роли, ресурсу или действию.
        """
        queryset = super().get_queryset()
        role_id = self.request.query_params.get('role_id')
        resource_id = self.request.query_params.get('resource_id')
        action_id = self.request.query_params.get('action_id')
        
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        if resource_id:
            queryset = queryset.filter(resource_id=resource_id)
        if action_id:
            queryset = queryset.filter(action_id=action_id)
        
        return queryset


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user roles (admin only).
    ViewSet для управления ролями пользователей (только для админов).
    """
    queryset = UserRole.objects.select_related('user', 'role').all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminPermission]
    
    def get_queryset(self):
        """
        Filter user roles by user or role.
        Фильтрация ролей пользователей по пользователю или роли.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        role_id = self.request.query_params.get('role_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        return queryset


@api_view(['GET'])
@permission_classes([IsAdminPermission])
def access_overview(request):
    """
    Get overview of access control system.
    Получение обзора системы контроля доступа.
    """
    roles_count = Role.objects.count()
    resources_count = Resource.objects.count()
    actions_count = Action.objects.count()
    permissions_count = Permission.objects.count()
    user_roles_count = UserRole.objects.count()
    
    return Response({
        'roles': roles_count,
        'resources': resources_count,
        'actions': actions_count,
        'permissions': permissions_count,
        'user_roles': user_roles_count
    }, status=status.HTTP_200_OK)
