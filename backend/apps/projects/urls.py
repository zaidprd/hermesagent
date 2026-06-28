from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("new/", views.project_create, name="create"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("<int:pk>/settings/", views.project_settings, name="settings"),
    path("<int:pk>/threads/", views.project_threads_settings, name="threads_settings"),
]
