"""
User models for custom authentication system.
Модели пользователей для кастомной системы аутентификации.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager.
    Кастомный менеджер пользователей.
    """
    
    def create_user(self, email, full_name, password=None, **extra_fields):
        """
        Create and save a regular user.
        Создание и сохранение обычного пользователя.
        """
        if not email:
            raise ValueError('The Email field must be set / Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Create and save a superuser.
        Создание и сохранение суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True. / Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True. / Суперпользователь должен иметь is_superuser=True.')
        
        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Custom user model.
    Кастомная модель пользователя.
    """
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User / Пользователь'
        verbose_name_plural = 'Users / Пользователи'
    
    def __str__(self):
        return f'{self.full_name} ({self.email})'
    
    def has_perm(self, perm, obj=None):
        """
        Django admin permission check.
        Проверка прав для Django admin.
        """
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        """
        Django admin permission check.
        Проверка прав для Django admin.
        """
        return self.is_superuser
