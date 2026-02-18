from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "account_type", "is_active", "is_staff")
    list_filter = ("account_type", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
