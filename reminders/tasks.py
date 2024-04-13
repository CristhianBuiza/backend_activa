from app.fcm import send_push_notification
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_reminder_notification(user_id, description, notify_time):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    profile = user.profile  # Asumiendo que el perfil está vinculado directamente al usuario como user.profile
    if profile.device_token:
        # Revisa si el momento de notificación coincide con el tiempo actual
        current_time = timezone.now()
        if current_time >= notify_time - timedelta(minutes=1) and current_time <= notify_time + timedelta(minutes=1):
            send_push_notification(profile.device_token, "Recordatorio", description)
