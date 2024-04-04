from django.contrib import admin
from help.forms import RequestAttentionForm
from help.models import Help, RequestAttention
from django.db.models import Q

def marcar_como_en_proceso(queryset):
    queryset.update(estado='en proceso')

def marcar_como_finalizado(queryset):
    queryset.update(estado='finalizado')

marcar_como_en_proceso.short_description = "Marcar como En proceso"
marcar_como_finalizado.short_description = "Marcar como Finalizado"

@admin.register(RequestAttention)
class RequestAttentionAdmin(admin.ModelAdmin):
    form = RequestAttentionForm
    list_display = ('date_of_attention', 'time_of_attention', 'PAMid', 'user', 'type', 'telefono_de_contacto', 'estado', 'atendido_por', 'details')
    search_fields = ('user__username', 'PAMid')
    actions = [marcar_como_en_proceso, marcar_como_finalizado]
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['estado'].widget.can_add_related = False 
        return form

@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'scream', 'details', 'state')
# Resto del código…
