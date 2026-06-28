from django.urls import path

from . import api_views

app_name = "jobs_api"

urlpatterns = [
    path("jobs/claim/", api_views.claim_job, name="claim"),
    path("jobs/<int:pk>/complete/", api_views.complete_job, name="complete"),
    path("jobs/<int:pk>/fail/", api_views.fail_job, name="fail"),
]
