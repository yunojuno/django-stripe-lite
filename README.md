# django-stripe-lite

Provides a light-touch Django integration with Stripe.

We handle Stripe webhook security & persisting all events, while allowing your project to take care
of the business logic.

Requires PostgreSQL, Python 3.x & Django 3.x.

## Getting started

```bash
pip install django-stripe-lite
```

**Include the app in your INSTALLED_APPS setting:**

```python
INSTALLED_APPS = (
    ...,
    "django_stripe",
)
```

**Include the URLs in your URL conf:**

```python
from django.urls import include, path

urlpatterns = [
    # Assuming we're at the root, this will make the webhook
    # available at /stripe/webhook/
    path("stripe/", include("django_stripe.urls", namespace="stripe"))
]
```

**Set the required settings in your settings file:**

```python
STRIPE_WEBHOOK_SECRET = "whsec_0DoBceBjS0jjm7aQj459FXiFSluJEBxt"
```

**Run the migrations:**

```bash
python manage.py migrate django_stripe
```

**Set up your event handlers:**

If all registered event handlers pass successfully, then the webhook event will be persisted to the
database. If not, the webhook view will deliberately raise and roll back the transaction.

```python
from django_stripe.models import WebhookEvent
from django_stripe.webhooks import stripe_webhook_handler

# Single event handler
@stripe_webhook_handler("customer.subscription.deleted")
def delete_customer_subscription(event: WebhookEvent) -> Any:
    # event.data (dict, Stripe Event object.data field, the object which triggered the webhook event)
    # event.event_type (str, the full event type name e.g customer.subscription.deleted)
    # event.mode (textchoices, LIVE or TEST)
    # event.stripe_created_at (datetime, when Stripe created the event)
    # event.db_created_at (datetime, when the database initially saved the event)
    # event.db_last_updated_at (datetime, when the database last saved the event)
    # event.stripe_id (str, Stripe Event ID)
    # event.api_version (str, Stripe API version)
    # event.request_id (str, the Stripe ID of the instigating request, if available)
    # event.request_idempotency_key (str, the idempotency key of the instigating request, if available)
    # event.is_processed (bool, whether the event was processed by a handler successfully)
    # event.headers (dict, the headers of the webhook request)
    # event.remote_ip (str, Remote IP of the webhook request)
    pass

# Multiple event handler
@stripe_webhook_handler(
    "customer.subscription.created",
    "customer.subscription.deleted",
    "customer.subscription.updated",
)
def customer_handler(event: WebhookEvent) -> Any:
    # See notes above for event structure.
    pass
```

That's it, you should be able to start receiving webhook events with the Stripe CLI test client.
Then once you're ready, setup the production webhook via the Stripe dashboard.

## Tests

#### Running tests

The tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment,
you can run them:

```bash
$ poetry run pytest
```

The CI suite is controlled by `tox`, which contains a set of environments that will format (`fmt`),
lint, and test against all supported Python + Django version combinations.

```bash
$ tox
```

#### CI

CI is handled by GitHub Actions. See the Actions tab on Github & the `.github/workflows` folder.
