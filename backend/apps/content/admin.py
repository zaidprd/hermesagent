from django.contrib import admin

from .models import Article, Keyword, Title


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("keyword", "project", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("keyword", "project__name")


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "is_duplicate", "created_at")
    list_filter = ("status", "is_duplicate")
    search_fields = ("title", "project__name")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "word_count", "created_at")
    list_filter = ("status",)
    search_fields = ("title__title", "project__name")
