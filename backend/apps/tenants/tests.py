from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.tenants.models import Tenant

User = get_user_model()


class TenantAutoCreateTests(TestCase):
    def test_tenant_created_on_signup(self):
        user = User.objects.create_user(email="a@example.com", password="pw12345!")
        self.assertTrue(hasattr(user, "tenant"))
        self.assertEqual(Tenant.objects.filter(owner=user).count(), 1)

    def test_duplicate_names_get_unique_slugs(self):
        u1 = User.objects.create_user(email="s1@example.com", password="pw12345!")
        u2 = User.objects.create_user(email="s2@example.com", password="pw12345!")
        for u in (u1, u2):
            u.tenant.name = "Same Name"
            u.tenant.slug = ""
            u.tenant.save()
        self.assertNotEqual(u1.tenant.slug, u2.tenant.slug)
