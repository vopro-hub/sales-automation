from django.contrib import admin
from .models import Tenant, User

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "is_active")
    search_fields = ("name", "whatsapp_number")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "staff_ID", "first_name", "last_name", "email", "whatsapp_number", "is_active")
    search_fields = ("username", "staff_id")

