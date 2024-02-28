from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ('P.A.M', 'P.A.M'),
        ('Entorno', 'Entorno'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True) 
    def __str__(self):
        return self.user.username