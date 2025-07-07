import os

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'jota_news.settings.development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

from .celery import app as celery_app

__all__ = ('celery_app',)
