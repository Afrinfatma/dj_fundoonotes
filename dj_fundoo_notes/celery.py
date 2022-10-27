import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_fundoo_notes.settings')

app = Celery('dj_fundoo_notes')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = 'redis://localhost:6379/0'
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

app.conf.broker_url = BASE_REDIS_URL