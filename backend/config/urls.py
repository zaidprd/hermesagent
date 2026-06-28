from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("app/", include("apps.dashboard.urls")),
    path("app/projects/", include("apps.projects.urls")),
    path("app/", include("apps.content.urls")),
    path("api/hermes/", include("apps.jobs.urls")),
    path("app/", include("apps.billing.urls")),
    path("", include("apps.core.urls")),
]
