from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Project(TimeStampedModel):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    # Content context — consumed when generating titles/articles.
    niche = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=64, default="Indonesia")
    tone = models.CharField(max_length=255, blank=True)
    target_audience = models.CharField(max_length=255, blank=True)

    # WordPress publish target
    wp_site_url = models.URLField(max_length=500, blank=True)
    wp_username = models.CharField(max_length=255, blank=True)
    wp_app_password = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "slug"],
                name="uniq_project_slug_per_tenant",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "project"
            slug = base
            i = 1
            siblings = Project.objects.filter(tenant=self.tenant)
            while siblings.exclude(pk=self.pk).filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.pk])

    def __str__(self):
        return self.name
