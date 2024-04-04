from django.db import models

class Help(models.Model):
    HELP_CHOICES = (
    ('pending', 'Pendiente'),
    ('completed', 'Completado'),
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Usuario')
    scream = models.CharField(max_length=100, verbose_name='Pantalla')
    details = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Detalles')
    state = models.CharField(max_length=100, choices=HELP_CHOICES, default='pending', verbose_name='Estado')
    date = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.scream
    
class RequestAttention(models.Model):
    SERVICE_CHOICES = (
    ('taxi', 'Taxi'),
    ('payment', 'Pago'),
    )
    SERVICE_STATUS = (
    ('pendiente', 'Pendiente'),
    ('en proceso', 'En proceso'),
    ('finalizado', 'Finalizado'),
    )
    type = models.CharField(max_length=100, choices=SERVICE_CHOICES, null=True, blank=True, verbose_name='Pantalla') 
    date_of_attention = models.DateField(auto_now_add=True, verbose_name='Fecha')
    time_of_attention = models.TimeField(auto_now=True, verbose_name='Hora')
    PAMid = models.CharField(max_length=100, verbose_name='PAM id') 
    telefono_de_contacto = models.CharField(max_length=100, verbose_name='Teléfono de Contacto')
    estado = models.CharField(max_length=100, choices=SERVICE_STATUS, null=True, blank=True, verbose_name='Estado') 
    atendido_por = models.CharField(max_length=100, verbose_name='Atendido Por')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Nombres y Apellidos')
    # user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Nombres y Apellidos')
    details = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Detalles')

    class Meta:
        verbose_name = 'Solicitud de Atención'
        verbose_name_plural = 'Solicitudes de Atención'

    def __str__(self):
        return f"{self.date_of_attention} - {self.type}"