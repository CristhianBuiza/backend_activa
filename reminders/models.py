from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User


# The Reminder class represents a reminder with a description, start and end time, date, and
# associated user.
class Reminder(models.Model):
    description = models.TextField()
    hour_start = models.TimeField()
    hour_end = models.TimeField()    
    day = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        date_time_start = datetime.datetime.combine(self.day, self.hour_start)
        notify_time_before = datetime.timezone.make_aware(date_time_start - datetime.timedelta(minutes=15))
        notify_time_exact = timezone.make_aware(date_time_start)

        # Programa las notificaciones
        from .tasks import send_reminder_notification
        send_reminder_notification.apply_async((self.user.id, self.description, notify_time_before), eta=notify_time_before)
        send_reminder_notification.apply_async((self.user.id, self.description, notify_time_exact), eta=notify_time_exact)

        super().save(*args, **kwargs) 