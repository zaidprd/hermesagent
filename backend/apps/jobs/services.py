from django.conf import settings

from .models import Job


def _project_context(project):
    return {
        "name": project.name,
        "niche": project.niche,
        "language": project.language,
        "tone": project.tone,
        "target_audience": project.target_audience,
    }


def enqueue_generate_title(keyword, n_titles=None):
    project = keyword.project
    payload = {
        "keyword_id": keyword.id,
        "keyword": keyword.keyword,
        "n_titles": n_titles or settings.HERMES_DEFAULT_TITLE_COUNT,
        "project": _project_context(project),
    }
    return Job.objects.create(
        tenant=project.tenant,
        agent_type="generate_title",
        payload=payload,
    )


def enqueue_generate_article(title):
    project = title.project
    payload = {
        "title_id": title.id,
        "title": title.title,
        "keyword": title.keyword.keyword,
        "n_words": getattr(settings, "HERMES_DEFAULT_ARTICLE_WORDS", 1200),
        "project": _project_context(project),
    }
    return Job.objects.create(
        tenant=project.tenant,
        agent_type="generate_article",
        payload=payload,
    )


def enqueue_publish_wordpress(article):
    project = article.project
    payload = {
        "article_id": article.id,
        "title": article.title.title,
        "body": article.body,
        "meta_description": article.meta_description,
        "featured_image_url": article.featured_image_url,
        "wp_site_url": project.wp_site_url,
        "wp_username": project.wp_username,
        "wp_app_password": project.wp_app_password,
    }
    return Job.objects.create(
        tenant=project.tenant,
        agent_type="publish_wordpress",
        payload=payload,
    )
