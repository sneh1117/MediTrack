from django.contrib import admin
from .models import Medication

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'dosage', 'frequency', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'frequency', 'start_date']
    search_fields = ['name', 'user__username', 'dosage']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'dosage')
        }),
        ('Schedule', {
            'fields': ('frequency', 'custom_schedule', 'start_date', 'end_date')
        }),
        ('Additional Info', {
            'fields': ('notes', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )