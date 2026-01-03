"""
Модели кастомной системы контроля доступа.
"""
from django.db import models
from django.conf import settings


class Role(models.Model):
    """Роль пользователя (например, admin, user, manager)."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    """Ресурс, к которому может быть предоставлен доступ (например, projects, reports, users)."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resources'
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Action(models.Model):
    """Действие, которое может быть выполнено над ресурсом (например, read, create, update, delete)."""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'actions'
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    """Правило доступа: Роль может выполнить Действие над Ресурсом."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Право доступа'
        verbose_name_plural = 'Права доступа'
        unique_together = [['role', 'resource', 'action']]
        ordering = ['role', 'resource', 'action']
    
    def __str__(self):
        return f'{self.role.name} может {self.action.name} {self.resource.name}'


class UserRole(models.Model):
    """Связь многие-ко-многим между User и Role."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        unique_together = [['user', 'role']]
        ordering = ['user', 'role']
    
    def __str__(self):
        return f'{self.user.email} - {self.role.name}'
