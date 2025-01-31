from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)


