from django.contrib import admin
from .models import Symptom

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'severity', 'date', 'logged_at']
    list_filter = ['severity', 'date', 'name']
    search_fields = ['name', 'notes', 'user__username']
    readonly_fields = ['logged_at']
    filter_horizontal = ['related_medications']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'severity', 'date')
        }),
        ('Details', {
            'fields': ('notes', 'related_medications')
        }),
        ('Timestamp', {
            'fields': ('logged_at',),
            'classes': ('collapse',)
        }),
    )