import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_automator.settings")

app = Celery("sales_automator")

app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks in all installed apps
app.autodiscover_tasks()
