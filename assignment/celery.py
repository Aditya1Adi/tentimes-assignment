# news_collector/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_collector.settings')

# Create a Celery instance and configure it using the settings module.
celery_app = Celery('news_collector')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps.
celery_app.autodiscover_tasks()
