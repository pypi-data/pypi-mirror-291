from django.urls import path, include

from . import views

app_name = "shopify_app_billing"


urlpatterns = [
    path("plans-redirect/", views.plans_redirect, name="plans"),
    path("activate-plan/", views.activate_plan, name="activate_plan"),
]
