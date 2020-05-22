"""
Webhook call handling.

Any function can register itself to handle a specific event
by using the @stripe_webhook_handler("event.name") syntax.

We deliberately maintain a 1:1 mapping between full event type
name and a function handler to keep things simple; it means that
given any full event name you can find all the handlers with a
grep.

It also means that if Stripe introduce a new sub-event, for a
parent event - then our handlers will not start automatically
receiving events for that new event type. This is a deliberate
design choice and differs from how djstripe handles handler
registration - so take care if migrating.

Do not rely on your handlers being called in the same order every
single time, as registration occurs on load - and it will be hard
for you to maintain any semblence of control. If you need actions
to happen in a specific order, then register one parent handler
and manage the code flow via that.

Usage:

    from django_stripe.models import WebhookEvent
    from django_stripe.webhooks import stripe_webhook_handler

    # Single event handler
    @stripe_webhook_handler("customer.subscription.deleted")
    def delete_customer_subscription(event: WebhookEvent) -> Any:
        pass

    # Multiple event handler
    @stripe_webhook_handler(
        "customer.subscription.created",
        "customer.subscription.deleted",
        "customer.subscription.updated",
    )
    def customer_handler(event: WebhookEvent) -> Any:
        pass
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from .models import WebhookEvent


__all__ = ["stripe_webhook_handler", "run_handlers"]


REGISTRY: defaultdict = defaultdict(list)


def stripe_webhook_handler(*event_types: List[str]) -> Callable:
    """
    Decorate a function to register it as a Stripe webhook handler.

    Functions must be registered against the full Stripe event name
    (e.g. 'customer.subscription.deleted') that they wish to handle.
    To handle multiple, pass extra full event type names as arguments.
    """

    def decorator(func: Callable) -> Callable:
        for event_type in event_types:
            REGISTRY[event_type].append(func)
        return func

    return decorator


def run_handlers(event: WebhookEvent) -> None:
    """
    Invoke all handlers registered against a full event type name.

    Handlers for each event type group are invoked in order of
    registration and as that cannot be guaranteed easily - the
    handlers should not be order-dependent, see the module note.
    """
    handlers = REGISTRY.get(event.event_type, [])
    if not handlers:
        return

    for handler_func in handlers:
        handler_func(event=event)

    event.mark_processed()
    event.save(update_fields=["state", "db_last_updated_at"])
