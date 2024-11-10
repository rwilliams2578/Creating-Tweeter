from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Add date_of_birth to the fieldsets


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    Adds date_of_birth field to the user form.
    """

    fieldsets = UserAdmin.fieldsets + (("Additional Info", {"fields": ("date_of_birth",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
