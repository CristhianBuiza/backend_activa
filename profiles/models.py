from tabnanny import verbose
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
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True, default='P.A.M') 
    cellphone = models.CharField(max_length=100, null=True, blank=True)
    additionalCellphone = models.CharField(max_length=100, null=True, blank=True)
    pams = models.ManyToManyField('self', symmetrical=False, related_name='entornos', blank=True)
    @property
    def email(self):
        return self.user.email
    @property
    def username(self):
        return self.user.username
    @property
    def first_name(self):
        return self.user.first_name
    @property
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    
    def __str__(self):
        return self.user.username
    