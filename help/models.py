from django.db import models

# Create your models here.
class Help(models.Model):
    
    HELP_CHOICES = (
    ('pending', 'Pendiente'),
    ('completed', 'Completado'),
    )
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    scream=models.CharField(max_length=100)
    details = models.TextField(max_length=1000, blank=True, null=True)
    state = models.CharField(max_length=100, choices=HELP_CHOICES, default='pending')
    date=models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.scream
    
class RequestAttention(models.Model):
    # choice taxi, payment - en espanol deberia decir en las opciones Taxi y Pagos
    SERVICE_CHOICES = (
    ('taxi', 'Taxi'),
    ('payment', 'Pago'),
    )
    type = models.CharField(max_length=100, choices=SERVICE_CHOICES, null=True, blank=True, verbose_name='Tipo de Servicio') 
    date_of_attention=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Atención')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Usuario')
    details = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Detalles')

    class Meta:
        verbose_name = 'Solitud de Atención'
        verbose_name_plural = 'Solitudes de Atención'
    def __str__(self):
        return self.date