from django.contrib import admin
from .models import TagCommunity, Community
# Register your models here.
admin.site.register(Community)
admin.site.register(TagCommunity)