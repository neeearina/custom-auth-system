"""
WSGI config for custom-auth-system project.
Конфигурация WSGI для проекта custom-auth-system.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

