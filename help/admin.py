from django.contrib import admin
from help.forms import RequestAttentionForm
from help.models import Help, RequestAttention

# Register your models here.
# @admin.register(Help)
admin.site.register(Help)

from django.contrib import admin
from .models import RequestAttention
from django.db.models import Q

@admin.register(RequestAttention)
class RequestAttentionAdmin(admin.ModelAdmin):
    form = RequestAttentionForm
