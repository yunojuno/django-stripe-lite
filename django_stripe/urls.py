from django.urls import path

from .webhook_view import webhook_view

app_name = "stripe"

urlpatterns = [path("webhook/", webhook_view, name="webhook")]
