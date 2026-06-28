"""Side effects to run when a Hermes job finishes."""
from django.utils.text import slugify

from apps.content.models import Article, Keyword, Title


def _get_keyword(job):
    keyword_id = (job.payload or {}).get("keyword_id")
    if not keyword_id:
        return None
    return Keyword.objects.select_related("project").filter(pk=keyword_id).first()


def on_generate_title_completed(job):
    keyword = _get_keyword(job)
    if keyword is None:
        return
    project = keyword.project
    titles = (job.result or {}).get("titles") or []

    existing_slugs = set(
        Title.objects.filter(project=project).values_list("slug", flat=True)
    )
    seen = set()
    new_titles = []
    for raw in titles:
        text = (raw or "").strip()
        if not text:
            continue
        slug = slugify(text)[:255]
        is_dup = slug in existing_slugs or slug in seen
        seen.add(slug)
        new_titles.append(
            Title(
                keyword=keyword,
                project=project,
                title=text[:255],
                slug=slug,
                is_duplicate=is_dup,
            )
        )
    if new_titles:
        Title.objects.bulk_create(new_titles)

    keyword.status = Keyword.DONE
    keyword.save(update_fields=["status", "updated_at"])


def on_generate_title_failed(job):
    keyword = _get_keyword(job)
    if keyword is not None:
        keyword.status = Keyword.PENDING
        keyword.save(update_fields=["status", "updated_at"])


def on_generate_article_completed(job):
    title_id = (job.payload or {}).get("title_id")
    if not title_id:
        return
    title = Title.objects.select_related("project").filter(pk=title_id).first()
    if not title:
        return
    result = job.result or {}
    Article.objects.update_or_create(
        title=title,
        defaults={
            "project": title.project,
            "body": result.get("body", ""),
            "meta_description": result.get("meta_description", ""),
            "featured_image_url": result.get("featured_image_url", ""),
            "image_prompt": result.get("image_prompt", ""),
            "word_count": result.get("word_count", 0),
            "status": Article.DONE,
        },
    )


def on_generate_article_failed(job):
    title_id = (job.payload or {}).get("title_id")
    if not title_id:
        return
    Article.objects.filter(title_id=title_id).update(status=Article.FAILED)


def on_publish_wordpress_completed(job):
    article_id = (job.payload or {}).get("article_id")
    if not article_id:
        return
    result = job.result or {}
    Article.objects.filter(pk=article_id).update(
        publish_status=Article.PUBLISH_PUBLISHED,
        wp_post_id=result.get("post_id"),
        wp_post_url=result.get("post_url", ""),
    )


def on_publish_wordpress_failed(job):
    article_id = (job.payload or {}).get("article_id")
    if not article_id:
        return
    Article.objects.filter(pk=article_id).update(publish_status=Article.PUBLISH_FAILED)


def on_post_threads_completed(job):
    article_id = (job.payload or {}).get("article_id")
    if not article_id:
        return
    result = job.result or {}
    Article.objects.filter(pk=article_id).update(
        threads_status=Article.THREADS_POSTED,
        threads_post_id=result.get("post_id", ""),
        threads_post_url=result.get("post_url", ""),
    )


def on_post_threads_failed(job):
    article_id = (job.payload or {}).get("article_id")
    if not article_id:
        return
    Article.objects.filter(pk=article_id).update(threads_status=Article.THREADS_FAILED)


_COMPLETED = {
    "generate_title": on_generate_title_completed,
    "generate_article": on_generate_article_completed,
    "publish_wordpress": on_publish_wordpress_completed,
    "post_threads": on_post_threads_completed,
}
_FAILED = {
    "generate_title": on_generate_title_failed,
    "generate_article": on_generate_article_failed,
    "publish_wordpress": on_publish_wordpress_failed,
    "post_threads": on_post_threads_failed,
}


def handle_completion(job):
    handler = _COMPLETED.get(job.agent_type)
    if handler:
        handler(job)


def handle_failure(job):
    handler = _FAILED.get(job.agent_type)
    if handler:
        handler(job)
