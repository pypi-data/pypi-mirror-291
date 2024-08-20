from django.urls import path

from django_ministripe import views


urlpatterns = [
    path("webhook", views.webhook, name="django_ministripe_webhook")
]
