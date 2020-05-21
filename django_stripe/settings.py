import stripe
from django.conf import settings

# Test mode keys - do not use directly.
_TEST_PUBLISHABLE_KEY = getattr(settings, "STRIPE_TEST_PUBLISHABLE_KEY", "")
_TEST_SECRET_KEY = getattr(settings, "STRIPE_TEST_SECRET_KEY", "")

# Live mode keys - do not use directly.
_LIVE_PUBLISHABLE_KEY = getattr(settings, "STRIPE_LIVE_PUBLISHABLE_KEY", "")
_LIVE_SECRET_KEY = getattr(settings, "STRIPE_LIVE_SECRET_KEY", "")

# Determines whether Stripe API requests are sent as
# test or live requests to Stripe's systems.
LIVE_MODE = getattr(settings, "STRIPE_LIVE_MODE", False)

# Exportable keys, which provide the default in the correct mode.
PUBLISHABLE_KEY = _LIVE_PUBLISHABLE_KEY if LIVE_MODE else _TEST_PUBLISHABLE_KEY
SECRET_KEY = _LIVE_SECRET_KEY if LIVE_MODE else _TEST_SECRET_KEY

# Webhook secret: used for signature validation.
WEBHOOK_SECRET = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")

# Webhook tolerance: the time window in seconds for which the
# inbound webhook event's signature should be consided valid
# for. Set to None to accept any timestamps (unadvisable).
WEBHOOK_TOLERANCE_SECONDS = getattr(
    settings, "STRIPE_WEBHOOK_TOLERANCE_SECONDS", stripe.Webhook.DEFAULT_TOLERANCE
)

API_VERSION = getattr(settings, "STRIPE_API_VERSION", "2020-03-02")
