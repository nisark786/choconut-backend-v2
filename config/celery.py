import os
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv 
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))
# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# Create Celery app
app = Celery("config", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/1")

# Load additional configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")



# Auto-discover tasks from all installed apps
app.autodiscover_tasks(['apps.accounts', 'apps.orders', 'apps.products', 'apps.admin_panel'])


app.conf.imports = [
    'apps.accounts.tasks',
    'apps.orders.tasks',
    'apps.admin_panel.tasks',
]