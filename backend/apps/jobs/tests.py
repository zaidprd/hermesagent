import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.content.models import Keyword, Title
from apps.jobs.models import Job
from apps.jobs.services import enqueue_generate_title
from apps.projects.models import Project

User = get_user_model()

AUTH = {"HTTP_AUTHORIZATION": "Bearer dev-hermes-token"}


class HermesApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="h@example.com", password="pw12345!")
        self.project = Project.objects.create(
            tenant=self.user.tenant, name="P", niche="fikih"
        )
        self.keyword = Keyword.objects.create(
            project=self.project, keyword="sholat tahajud", status=Keyword.PROCESSING
        )
        self.job = enqueue_generate_title(self.keyword)

    def test_claim_requires_token(self):
        resp = self.client.post(reverse("jobs_api:claim"))
        self.assertEqual(resp.status_code, 401)

    def test_claim_marks_running_then_empty(self):
        resp = self.client.post(reverse("jobs_api:claim"), **AUTH)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["agent_type"], "generate_title")
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, Job.RUNNING)

        resp2 = self.client.post(reverse("jobs_api:claim"), **AUTH)
        self.assertEqual(resp2.status_code, 204)

    def test_complete_creates_titles_marks_done_and_flags_duplicate(self):
        result = {
            "titles": [
                "Cara Sholat Tahajud",
                "Cara Sholat Tahajud",  # duplicate
                "Keutamaan Tahajud",
            ]
        }
        resp = self.client.post(
            reverse("jobs_api:complete", args=[self.job.id]),
            data=json.dumps({"result": result}),
            content_type="application/json",
            **AUTH,
        )
        self.assertEqual(resp.status_code, 200)

        self.job.refresh_from_db()
        self.keyword.refresh_from_db()
        self.assertEqual(self.job.status, Job.COMPLETED)
        self.assertEqual(self.keyword.status, Keyword.DONE)

        titles = Title.objects.filter(project=self.project)
        self.assertEqual(titles.count(), 3)
        self.assertEqual(titles.filter(is_duplicate=True).count(), 1)

    def test_fail_resets_keyword(self):
        resp = self.client.post(
            reverse("jobs_api:fail", args=[self.job.id]),
            data=json.dumps({"error": "boom"}),
            content_type="application/json",
            **AUTH,
        )
        self.assertEqual(resp.status_code, 200)
        self.job.refresh_from_db()
        self.keyword.refresh_from_db()
        self.assertEqual(self.job.status, Job.FAILED)
        self.assertEqual(self.keyword.status, Keyword.PENDING)
