import os
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv 
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("config")


app.config_from_object("django.conf:settings", namespace="CELERY")



app.autodiscover_tasks(['apps.accounts', 'apps.orders', 'apps.products', 'apps.admin_panel'])


app.conf.imports = [
    'apps.accounts.tasks',
    'apps.orders.tasks',
    'apps.admin_panel.tasks',
]