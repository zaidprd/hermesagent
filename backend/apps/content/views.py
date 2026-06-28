import markdown as md
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.billing.models import Subscription
from apps.jobs.services import enqueue_generate_article, enqueue_generate_title, enqueue_post_threads, enqueue_publish_wordpress
from apps.projects.models import Project

from .models import Article, Keyword, Title


@login_required
@require_POST
def keyword_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, tenant=request.user.tenant)
    text = (request.POST.get("keyword") or "").strip()
    if text:
        keyword = Keyword.objects.create(
            project=project, keyword=text, status=Keyword.PROCESSING
        )
        enqueue_generate_title(keyword)
    return redirect(project)


@login_required
def keyword_card(request, pk):
    """HTMX poll target: returns the keyword card (titles appear once done)."""
    keyword = get_object_or_404(
        Keyword.objects.prefetch_related("titles__article"),
        pk=pk,
        project__tenant=request.user.tenant,
    )
    return render(request, "content/_keyword_card.html", {"k": keyword})


def _set_title_status(request, pk, status):
    title = get_object_or_404(Title, pk=pk, project__tenant=request.user.tenant)
    title.status = status
    title.save(update_fields=["status", "updated_at"])
    return render(request, "content/_title_row.html", {"t": title})


@login_required
@require_POST
def title_approve(request, pk):
    return _set_title_status(request, pk, Title.APPROVED)


@login_required
@require_POST
def title_reject(request, pk):
    return _set_title_status(request, pk, Title.REJECTED)


@login_required
@require_POST
def article_generate(request, title_pk):
    title = get_object_or_404(
        Title.objects.select_related("keyword", "project"),
        pk=title_pk,
        project__tenant=request.user.tenant,
        status=Title.APPROVED,
    )
    sub, _ = Subscription.objects.get_or_create(tenant=request.user.tenant)
    if not sub.can_generate_article():
        return render(request, "content/_quota_exceeded.html", {"sub": sub}, status=200)

    article, created = Article.objects.get_or_create(
        title=title,
        defaults={"project": title.project, "status": Article.PROCESSING},
    )
    if not created and article.status == Article.FAILED:
        article.status = Article.PROCESSING
        article.save(update_fields=["status", "updated_at"])
        enqueue_generate_article(title)
        sub.increment_article_count()
    elif created:
        enqueue_generate_article(title)
        sub.increment_article_count()
    return render(request, "content/_article_card.html", {"article": article})


@login_required
def article_card(request, pk):
    """HTMX poll target for article generation status."""
    article = get_object_or_404(Article, pk=pk, project__tenant=request.user.tenant)
    return render(request, "content/_article_card.html", {"article": article})


@login_required
@require_POST
def article_publish(request, pk):
    article = get_object_or_404(
        Article.objects.select_related("project"),
        pk=pk,
        project__tenant=request.user.tenant,
        status=Article.DONE,
    )
    if article.publish_status not in (Article.PUBLISH_NONE, Article.PUBLISH_FAILED):
        return redirect(article)
    article.publish_status = Article.PUBLISH_PUBLISHING
    article.save(update_fields=["publish_status", "updated_at"])
    enqueue_publish_wordpress(article)
    return redirect(article)


@login_required
@require_POST
def article_post_threads(request, pk):
    article = get_object_or_404(
        Article.objects.select_related("project"),
        pk=pk,
        project__tenant=request.user.tenant,
        status=Article.DONE,
    )
    if article.threads_status not in (Article.THREADS_NONE, Article.THREADS_FAILED):
        return redirect(article)
    article.threads_status = Article.THREADS_POSTING
    article.save(update_fields=["threads_status", "updated_at"])
    enqueue_post_threads(article)
    return redirect(article)


@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, project__tenant=request.user.tenant)
    body_html = md.markdown(
        article.body,
        extensions=["extra", "nl2br"],
    )
    return render(
        request,
        "content/article_detail.html",
        {"article": article, "body_html": body_html},
    )
