from django.db import models

# Create your models here.
class Help(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    scream=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.date