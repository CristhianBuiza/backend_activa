import os
from app import settings
from pyfcm import FCMNotification

def send_push_notification(token, title, message):
    push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
    result = push_service.notify_single_device(registration_id=token, message_title=title, message_body=message)
    return result