import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

django.setup()


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