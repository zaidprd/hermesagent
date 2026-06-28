from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Keyword(TimeStampedModel):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (DONE, "Done"),
    ]

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="keywords",
    )
    keyword = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.keyword


class Title(TimeStampedModel):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    keyword = models.ForeignKey(
        Keyword,
        on_delete=models.CASCADE,
        related_name="titles",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="titles",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    is_duplicate = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        ordering = ["is_duplicate", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(TimeStampedModel):
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    STATUS_CHOICES = [
        (PROCESSING, "Processing"),
        (DONE, "Done"),
        (FAILED, "Gagal"),
    ]

    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name="article",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="articles",
    )
    body = models.TextField(blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    featured_image_url = models.URLField(max_length=2000, blank=True)
    image_prompt = models.TextField(blank=True)
    word_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)

    # WordPress publish tracking
    PUBLISH_NONE = "none"
    PUBLISH_PUBLISHING = "publishing"
    PUBLISH_PUBLISHED = "published"
    PUBLISH_FAILED = "failed"
    PUBLISH_STATUS_CHOICES = [
        (PUBLISH_NONE, "Belum dipublish"),
        (PUBLISH_PUBLISHING, "Sedang publish…"),
        (PUBLISH_PUBLISHED, "Published"),
        (PUBLISH_FAILED, "Gagal"),
    ]
    publish_status = models.CharField(
        max_length=20, choices=PUBLISH_STATUS_CHOICES, default=PUBLISH_NONE
    )
    wp_post_id = models.PositiveIntegerField(null=True, blank=True)
    wp_post_url = models.URLField(max_length=2000, blank=True)

    # Threads post tracking
    THREADS_NONE = "none"
    THREADS_POSTING = "posting"
    THREADS_POSTED = "posted"
    THREADS_FAILED = "failed"
    THREADS_STATUS_CHOICES = [
        (THREADS_NONE, "Belum dipost"),
        (THREADS_POSTING, "Sedang posting…"),
        (THREADS_POSTED, "Terpost"),
        (THREADS_FAILED, "Gagal"),
    ]
    threads_status = models.CharField(
        max_length=20, choices=THREADS_STATUS_CHOICES, default=THREADS_NONE
    )
    threads_post_id = models.CharField(max_length=64, blank=True)
    threads_post_url = models.URLField(max_length=2000, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("content:article_detail", args=[self.pk])

    def __str__(self):
        return f"Article: {self.title.title}"
