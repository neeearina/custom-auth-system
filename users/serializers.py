"""
Сериализаторы для приложения users.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        """Проверка совпадения паролей."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают.'
            })
        return attrs
    
    def create(self, validated_data):
        """Создание нового пользователя."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Проверка учетных данных."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            if not user:
                raise serializers.ValidationError('Неверный email или пароль.')
            if not user.is_active:
                raise serializers.ValidationError('Учетная запись пользователя отключена.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Необходимо указать "email" и "password".')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'date_joined', 'last_login')
        read_only_fields = ('id', 'email', 'date_joined', 'last_login')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя."""
    
    class Meta:
        model = User
        fields = ('full_name',)

