from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Notification)
def send_notification_via_websocket(sender, instance, created, **kwargs):
    if created:  # Nos aseguramos de que la notificación es nueva
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",  # Este es el nombre del grupo. Asegúrate de que tus clientes se conecten a este grupo.
            {
                "type": "notification.message",  # Este método debe ser implementado en tu NotificationConsumer.
                "message": json.dumps({
                    "title": instance.title,
                    "body": instance.body,
                    "id": instance.id  # Opcionalmente, puedes enviar el ID o cualquier otro dato relevante.
                })
            }
        )
