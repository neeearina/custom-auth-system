"""
Сериализаторы для приложения access.
"""
from rest_framework import serializers
from .models import Role, Resource, Action, Permission, UserRole
from users.models import User


class ActionSerializer(serializers.ModelSerializer):
    """Сериализатор для Action."""
    
    class Meta:
        model = Action
        fields = ('id', 'name', 'description', 'created_at')
        read_only_fields = ('id', 'created_at')


class ResourceSerializer(serializers.ModelSerializer):
    """Сериализатор для Resource."""
    
    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для Role."""
    
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для Permission."""
    role = RoleSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)
    action = ActionSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False)
    resource_id = serializers.IntegerField(write_only=True, required=False)
    action_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Permission
        fields = (
            'id', 'role', 'resource', 'action',
            'role_id', 'resource_id', 'action_id', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def create(self, validated_data):
        """Создание права доступа с role_id, resource_id, action_id."""
        role_id = validated_data.pop('role_id')
        resource_id = validated_data.pop('resource_id')
        action_id = validated_data.pop('action_id')
        
        role = Role.objects.get(id=role_id)
        resource = Resource.objects.get(id=resource_id)
        action = Action.objects.get(id=action_id)
        
        return Permission.objects.create(
            role=role,
            resource=resource,
            action=action
        )


class UserRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для UserRole."""
    user = serializers.SerializerMethodField()
    role = RoleSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    role_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = UserRole
        fields = ('id', 'user', 'role', 'user_id', 'role_id', 'assigned_at')
        read_only_fields = ('id', 'assigned_at')
    
    def get_user(self, obj):
        """Возвращает email и полное имя пользователя."""
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'full_name': obj.user.full_name
        }
    
    def create(self, validated_data):
        """Создание роли пользователя с user_id и role_id."""
        user_id = validated_data.pop('user_id')
        role_id = validated_data.pop('role_id')
        
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        
        return UserRole.objects.create(user=user, role=role)


class PermissionListSerializer(serializers.Serializer):
    """Сериализатор для списка прав доступа с фильтрами."""
    role_id = serializers.IntegerField(required=False)
    resource_id = serializers.IntegerField(required=False)
    action_id = serializers.IntegerField(required=False)
