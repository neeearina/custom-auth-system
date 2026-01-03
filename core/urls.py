"""
Конфигурация URL для проекта custom-auth-system.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/access/', include('access.urls')),
    path('api/mock/', include('mock.urls')),
]

