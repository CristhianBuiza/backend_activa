from django.db import models

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=50)
    article = models.TextField()
    img = models.ImageField(upload_to='communities')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('TagCommunity', related_name='communities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class TagCommunity(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name