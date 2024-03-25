from django.contrib import admin
from .models import PayServices, Service, TagService, TaxiService
# Register your models here.
admin.site.register(Service)
admin.site.register(TagService)
admin.site.register(TaxiService)
admin.site.register(PayServices)