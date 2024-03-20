from django.contrib import admin
from .models import Service, TagService, TaxiService
# Register your models here.
admin.site.register(Service)
admin.site.register(TagService)
admin.site.register(TaxiService)

