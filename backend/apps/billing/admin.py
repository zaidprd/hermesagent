from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["tenant", "plan", "valid_until", "articles_this_month", "quota_month", "mayar_order_id"]
    list_filter = ["plan"]
    search_fields = ["tenant__name", "mayar_order_id"]
    readonly_fields = ["articles_this_month", "quota_month", "created_at", "updated_at"]
