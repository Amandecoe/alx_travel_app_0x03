import os

from celery import Celery

# Set default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')

#load settings from django using CELERY_namespace
app.config_from_object('django.conf:settings', namespace = 'CELERY')

# auto discover tasks from all installed apps
app.autodiscover_tasks()