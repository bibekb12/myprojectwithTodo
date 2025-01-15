import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProjectCelery.settings")

app = Celery("projectCelery")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
