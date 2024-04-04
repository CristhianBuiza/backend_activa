from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    affiliations = models.ManyToManyField('self', symmetrical=False, related_name='entornos', blank=True)
    
    def add_affiliation(self, profile):
        self.affiliations.add(profile)
        if profile.role == 'Entorno':
            profile.affiliations.add(self)
            profile.save()
        elif profile.role == 'P.A.M' and self.role == 'Entorno':
            self.affiliations.add(profile)
            self.save()
    
    def clean(self):
        super().clean()  
        if self.role:
            for pam in self.affiliations.all():
                if pam.role == self.role:  
                    raise ValidationError(f"Los {self.role} no pueden afiliarse a sí mismos.")

    def save(self, *args, **kwargs):
        creating = self._state.adding  # Verifica si el objeto es nuevo y está siendo creado
        super().save(*args, **kwargs)  # Primero guarda el objeto para asegurarte de que tiene un ID

        if creating:
            # Tu lógica que depende de que el objeto ya esté guardado
            if self.role == 'Entorno':
                for pam in self.affiliations.filter(role='P.A.M'):
                    pam.affiliations.add(self)
            elif self.role == 'P.A.M':
                for entorno in self.affiliations.filter(role='Entorno'):
                    entorno.affiliations.add(self)

        # Llama a clean después de guardar para realizar validaciones
        # Asegúrate de que cualquier validación aquí no intente guardar el objeto nuevamente
        self.clean()
                
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    
    def __str__(self):
        return self.user.username
    
