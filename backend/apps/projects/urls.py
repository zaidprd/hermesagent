from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("new/", views.project_create, name="create"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("<int:pk>/settings/", views.project_settings, name="settings"),
]
