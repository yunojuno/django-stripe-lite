import stripe
from django.apps import AppConfig as DjangoAppConfig

import django_stripe


class AppConfig(DjangoAppConfig):
    name = "django_stripe"
    verbose_name = "Stripe"
    default_auto_field = "django.db.models.AutoField"

    def ready(self) -> None:
        from . import settings

        # Stripe library setup
        stripe.api_key = settings.SECRET_KEY
        stripe.api_version = settings.API_VERSION

        # Identify the plugin to Stripe
        stripe.set_app_info(
            "django-stripe-lite",
            version=django_stripe.__version__,
            url="https://github.com/yunojuno/django-stripe-lite",
        )
