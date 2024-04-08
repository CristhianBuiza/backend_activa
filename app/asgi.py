# We had before
# import os
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
# application = get_asgi_application()

import os

from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from notifications.consumers import NotificationConsumer
from .routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django_asgi_app = get_asgi_application()

import app.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path("ws/notifications/", NotificationConsumer.as_asgi()),
    ])
})