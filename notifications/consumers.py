# Asegúrate de que esta clase está definida en tu consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # El cliente se une al grupo 'notifications'
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # El cliente se va del grupo 'notifications'
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    # Este método corresponde al tipo 'notification.message' en tu signal
    async def notification_message(self, event):
        # Envía el mensaje a WebSocket
        await self.send(text_data=event["message"])
