import stripe
from django.apps import AppConfig

__version__ = "0.1.0"

default_app_config = "django_stripe.DjangoStripeAppConfig"


class DjangoStripeAppConfig(AppConfig):

    name = "django_stripe"
    verbose_name = "django-stripe-lite"

    def ready(self) -> None:
        from . import settings

        # Stripe library setup
        stripe.api_key = settings.SECRET_KEY
        stripe.api_version = settings.API_VERSION

        # Identify the plugin to Stripe
        stripe.set_app_info(
            "django-stripe-lite",
            version=__version__,
            url="https://github.com/yunojuno/django-stripe-lite",
        )
