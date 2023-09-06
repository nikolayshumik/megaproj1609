from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analogkufar.settings')
app = Celery('analogkufar')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()