from django.contrib import admin
from help.forms import RequestAttentionForm
from help.models import Help, RequestAttention

# Register your models here.
# @admin.register(Help)

from django.contrib import admin
from .models import RequestAttention
from django.db.models import Q

admin.site.register(Help)

@admin.register(RequestAttention)
class RequestAttentionAdmin(admin.ModelAdmin):
    form = RequestAttentionForm
