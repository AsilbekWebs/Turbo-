from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha', {'fields': ('email', 'phone', 'role')}),
    )