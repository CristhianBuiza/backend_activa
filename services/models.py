from django.db import models

# Create your models here.
class Service(models.Model):
    img = models.ImageField(upload_to='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('TagService', related_name='services')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class TagService(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name