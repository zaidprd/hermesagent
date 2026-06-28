from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DashboardAccessTests(TestCase):
    def test_anonymous_redirected(self):
        resp = self.client.get(reverse("dashboard:home"))
        self.assertEqual(resp.status_code, 302)

    def test_authenticated_ok(self):
        user = User.objects.create_user(email="d@example.com", password="pw12345!")
        self.client.force_login(user)
        resp = self.client.get(reverse("dashboard:home"))
        self.assertEqual(resp.status_code, 200)
