"""
ASGI config for config project.
"""

import os
import django

# Set Django settings FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# Initialize Django BEFORE importing anything that uses models
django.setup()

# NOW import everything else
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.accounts.middleware import JWTAuthMiddleware
import apps.notifications.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            apps.notifications.routing.websocket_urlpatterns
        )
    ),
})