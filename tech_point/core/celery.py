import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tech_point.settings")

app = Celery("tech_point")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
