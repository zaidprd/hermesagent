from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.projects.models import Project

User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(email="o1@example.com", password="pw12345!")
        self.u2 = User.objects.create_user(email="o2@example.com", password="pw12345!")
        self.p1 = Project.objects.create(tenant=self.u1.tenant, name="P1")

    def test_other_tenant_gets_404(self):
        self.client.force_login(self.u2)
        resp = self.client.get(reverse("projects:detail", args=[self.p1.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_owner_can_view(self):
        self.client.force_login(self.u1)
        resp = self.client.get(reverse("projects:detail", args=[self.p1.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_unique_slug_per_tenant(self):
        a = Project.objects.create(tenant=self.u1.tenant, name="Blog SEO")
        b = Project.objects.create(tenant=self.u1.tenant, name="Blog SEO")
        self.assertNotEqual(a.slug, b.slug)

    def test_create_assigns_current_tenant(self):
        self.client.force_login(self.u2)
        resp = self.client.post(reverse("projects:create"), {"name": "New One"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            Project.objects.filter(tenant=self.u2.tenant, name="New One").exists()
        )
