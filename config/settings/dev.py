from .base import *
from decouple import config


DEBUG = True

ALLOWED_HOSTS = [
    "13.60.70.161", 
    "13.60.70.161.nip.io", 
    "localhost", 
    "127.0.0.1",
    "0.0.0.0"
]


# CORS (React Dev Server)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://13.60.70.161",
    "http://13.60.70.161.nip.io",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://13.60.70.161",
    "http://13.60.70.161.nip.io"
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


FRONTEND_URL = "http://13.60.70.161.nip.io"



