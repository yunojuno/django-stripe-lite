import stripe
from django.conf import settings

# Determines whether Stripe API requests are sent as
# test or live requests to Stripe's systems.
LIVE_MODE = getattr(settings, "STRIPE_LIVE_MODE", False)

# Exportable keys
PUBLISHABLE_KEY = getattr(settings, "STRIPE_PUBLISHABLE_KEY", "")
SECRET_KEY = getattr(settings, "STRIPE_SECREY_KEY", "")

# Webhook secret: used for signature validation.
WEBHOOK_SECRET = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")

# Webhook tolerance: the time window in seconds for which the
# inbound webhook event's signature should be consided valid
# for. Set to None to accept any timestamps (unadvisable).
WEBHOOK_TOLERANCE_SECONDS = getattr(
    settings, "STRIPE_WEBHOOK_TOLERANCE_SECONDS", stripe.Webhook.DEFAULT_TOLERANCE
)

API_VERSION = getattr(settings, "STRIPE_API_VERSION", "2020-03-02")
