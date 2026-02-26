from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'assigned_doctor', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    
    # Add role to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'date_of_birth', 'assigned_doctor')}),
    )
    
    # Add role to add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'date_of_birth')}),
    )


from django.db import migrations

def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='sneh111').exists():
        User.objects.create_superuser(
            username='sneh111',
            email='sneh111@meditrack.com',
            password='ChemburGal123*'
        )

create_superuser()

