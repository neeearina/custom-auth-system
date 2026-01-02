"""
Custom access control models.
Модели кастомной системы контроля доступа.
"""
from django.db import models
from django.conf import settings


class Role(models.Model):
    """
    User role (e.g., admin, user, manager).
    Роль пользователя (например, admin, user, manager).
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role / Роль'
        verbose_name_plural = 'Roles / Роли'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Resource that can be accessed (e.g., projects, reports, users).
    Ресурс, к которому может быть предоставлен доступ (например, projects, reports, users).
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resources'
        verbose_name = 'Resource / Ресурс'
        verbose_name_plural = 'Resources / Ресурсы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Action(models.Model):
    """
    Action that can be performed on a resource (e.g., read, create, update, delete).
    Действие, которое может быть выполнено над ресурсом (например, read, create, update, delete).
    """
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'actions'
        verbose_name = 'Action / Действие'
        verbose_name_plural = 'Actions / Действия'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    Permission rule: Role can perform Action on Resource.
    Правило доступа: Роль может выполнить Действие над Ресурсом.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission / Право доступа'
        verbose_name_plural = 'Permissions / Права доступа'
        unique_together = [['role', 'resource', 'action']]
        ordering = ['role', 'resource', 'action']
    
    def __str__(self):
        return f'{self.role.name} can {self.action.name} {self.resource.name} / {self.role.name} может {self.action.name} {self.resource.name}'


class UserRole(models.Model):
    """
    Many-to-many relationship between User and Role.
    Связь многие-ко-многим между User и Role.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role / Роль пользователя'
        verbose_name_plural = 'User Roles / Роли пользователей'
        unique_together = [['user', 'role']]
        ordering = ['user', 'role']
    
    def __str__(self):
        return f'{self.user.email} - {self.role.name}'
