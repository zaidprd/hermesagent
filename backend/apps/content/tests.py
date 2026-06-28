from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Keyword, Title
from apps.jobs.models import Job
from apps.projects.models import Project

User = get_user_model()


class KeywordTitleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="c@example.com", password="pw12345!")
        self.project = Project.objects.create(tenant=self.user.tenant, name="P")
        self.client.force_login(self.user)

    def test_keyword_create_enqueues_job(self):
        resp = self.client.post(
            reverse("content:keyword_create", args=[self.project.pk]),
            {"keyword": "sholat"},
        )
        self.assertEqual(resp.status_code, 302)
        keyword = Keyword.objects.get(project=self.project)
        self.assertEqual(keyword.status, Keyword.PROCESSING)
        self.assertTrue(
            Job.objects.filter(
                agent_type="generate_title", tenant=self.user.tenant
            ).exists()
        )

    def test_approve_then_reject(self):
        keyword = Keyword.objects.create(project=self.project, keyword="x")
        title = Title.objects.create(keyword=keyword, project=self.project, title="Judul A")

        resp = self.client.post(reverse("content:title_approve", args=[title.pk]))
        self.assertEqual(resp.status_code, 200)
        title.refresh_from_db()
        self.assertEqual(title.status, Title.APPROVED)

        self.client.post(reverse("content:title_reject", args=[title.pk]))
        title.refresh_from_db()
        self.assertEqual(title.status, Title.REJECTED)

    def test_other_tenant_cannot_approve(self):
        keyword = Keyword.objects.create(project=self.project, keyword="x")
        title = Title.objects.create(keyword=keyword, project=self.project, title="Judul A")

        other = User.objects.create_user(email="o2@example.com", password="pw12345!")
        self.client.force_login(other)
        resp = self.client.post(reverse("content:title_approve", args=[title.pk]))
        self.assertEqual(resp.status_code, 404)
