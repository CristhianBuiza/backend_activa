from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('get_username', 'get_email',)  # Añade los métodos de solo lectura aquí

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    list_display = ('get_username', 'get_first_name', 'get_last_name' , 'role', 'get_email')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'role')
    list_filter = ('role',)
    list_per_page = 10