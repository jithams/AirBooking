from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'approval_status', 'is_staff')
    list_filter = ('approval_status', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Approval', {'fields': ('approval_status',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
