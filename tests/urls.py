from django.urls import include, path

urlpatterns = [path("stripe/", include("django_stripe.urls", namespace="stripe"))]
