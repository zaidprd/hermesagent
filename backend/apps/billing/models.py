from datetime import date, timedelta

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Subscription(TimeStampedModel):
    FREE = "free"
    PRO = "pro"
    PLAN_CHOICES = [(FREE, "Free"), (PRO, "Pro")]

    tenant = models.OneToOneField(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=FREE)
    valid_until = models.DateField(null=True, blank=True)
    articles_this_month = models.PositiveIntegerField(default=0)
    quota_month = models.DateField(default=date.today)
    mayar_order_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.tenant} — {self.plan}"

    def is_pro_active(self):
        if self.plan != self.PRO:
            return False
        if self.valid_until is None:
            return True
        return date.today() <= self.valid_until

    def _maybe_reset_quota(self):
        current_month_start = date.today().replace(day=1)
        if self.quota_month != current_month_start:
            self.articles_this_month = 0
            self.quota_month = current_month_start
            self.save(update_fields=["articles_this_month", "quota_month", "updated_at"])

    @property
    def free_limit(self):
        return getattr(settings, "BILLING_FREE_ARTICLE_LIMIT", 10)

    def can_generate_article(self):
        if self.is_pro_active():
            return True
        self._maybe_reset_quota()
        return self.articles_this_month < self.free_limit

    def increment_article_count(self):
        self._maybe_reset_quota()
        Subscription.objects.filter(pk=self.pk).update(
            articles_this_month=models.F("articles_this_month") + 1
        )
        self.refresh_from_db(fields=["articles_this_month"])

    def activate_pro(self, order_id="", days=30):
        self.plan = self.PRO
        self.valid_until = date.today() + timedelta(days=days)
        self.mayar_order_id = order_id
        self.save(update_fields=["plan", "valid_until", "mayar_order_id", "updated_at"])
