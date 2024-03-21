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
    
class ServiceIcon(models.Model):
    image = models.ImageField(upload_to='icons-service')

    def __str__(self):
        return f"Icon #{self.id}"

class TaxiService(models.Model):
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    origin=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=5, decimal_places=2)
    icon = models.ForeignKey(ServiceIcon, on_delete=models.SET_NULL, null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
class AttentionTaxiService(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    taxi_service = models.ForeignKey(TaxiService, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
# class RestaurantBrandService(models.Model):
#     title = models.CharField(max_length=100)
#     icon = models.ForeignKey(ServiceIcon, on_delete=models.SET_NULL, null=True, blank=True)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
# class DishService(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(RestaurantBrandService, on_delete=models.CASCADE)
#     tag = models.ManyToManyField('TagService', related_name='dishes')  
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.title

class PayServices(models):
    service = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    photo=models.ImageField(upload_to='payservices')
    
    def __str__(self):
        return self.service