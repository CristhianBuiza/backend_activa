from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Health(models.Model):
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to='health_documents')
    day = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name