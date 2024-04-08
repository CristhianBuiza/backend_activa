from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def send_notification(request):
    # Aquí crearías la notificación y la guardarías en la base de datos si es necesario
    # Por ejemplo: notification = Notification.objects.create(...)

    channel_layer = get_channel_layer()
    # Asegúrate de que el tipo de mensaje corresponda al manejador en tu consumer
    async_to_sync(channel_layer.group_send)(
        "notifications",  # Nombre del grupo; asegúrate de que coincida con el usado en tu Consumer
        {
            "type": "notification.message",  # Este método debe estar definido en tu NotificationConsumer
            "message": json.dumps({"title": "Nueva Notificación", "body": "Aquí el cuerpo de la notificación."})
        }
    )
    return JsonResponse({"success": True})
