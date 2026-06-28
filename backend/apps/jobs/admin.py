from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "agent_type", "status", "tenant", "created_at", "completed_at")
    list_filter = ("status", "agent_type")
    search_fields = ("agent_type", "tenant__name")
    readonly_fields = ("created_at", "updated_at", "started_at", "completed_at")
