from django.urls import path
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/reminders/', NotificationConsumer.as_asgi()),
]