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