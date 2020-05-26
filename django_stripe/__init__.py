import stripe
from django.apps import AppConfig as DjangoAppConfig

__version__ = "0.2.0"

default_app_config = "django_stripe.AppConfig"


class AppConfig(DjangoAppConfig):

    name = "django_stripe"
    verbose_name = "Stripe"

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
