from .base import *
from decouple import config
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load the .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# DATABASE (DEV)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# CORS (React Dev Server)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]



# SECURITY (Relaxed for dev)
SECURE_SSL_REDIRECT = False


# EMAIL CONFIGURATION (Gmail SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = f"Choconut <{EMAIL_HOST_USER}>"


FRONTEND_URL = "http://localhost:5173"  # dev



