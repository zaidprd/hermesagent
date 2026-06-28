from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tenant


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_tenant_for_user(sender, instance, created, **kwargs):
    """Give every new user their own workspace."""
    if created:
        label = instance.name or instance.email.split("@")[0]
        Tenant.objects.create(owner=instance, name=f"Workspace {label}")
