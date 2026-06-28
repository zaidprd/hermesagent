from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "tenant", "created_at")
    search_fields = ("name", "slug", "tenant__name")
    list_filter = ("tenant",)
