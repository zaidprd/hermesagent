from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("billing/", views.billing_overview, name="overview"),
    path("billing/webhook/mayar/", views.mayar_webhook, name="mayar_webhook"),
]
