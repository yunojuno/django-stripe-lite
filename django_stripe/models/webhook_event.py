from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

import stripe
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils.request import get_client_ip
from .base import StripeModel

if TYPE_CHECKING:
    from django.http import HttpRequest


class WebhookEventQuerySet(models.QuerySet):
    def live(self) -> WebhookEventQuerySet:
        return self.filter(mode=WebhookEvent.Mode.LIVE)

    def test(self) -> WebhookEventQuerySet:
        return self.filter(mode=WebhookEvent.Mode.TEST)

    def received(self) -> WebhookEventQuerySet:
        return self.filter(state=WebhookEvent.State.RECEIVED)

    def processed(self) -> WebhookEventQuerySet:
        return self.filter(state=WebhookEvent.State.PROCESSED)


class WebhookEventManager(models.Manager):
    def create_from_event(
        self, request: HttpRequest, event: stripe.Event
    ) -> WebhookEvent:
        mode = WebhookEvent.Mode.from_stripe_livemode(event.livemode)
        stripe_created_at = dt.datetime.fromtimestamp(event.created)
        remote_ip = get_client_ip(request)

        stripe_request = event.get("request")
        request_id = stripe_request.id or ""
        request_idempotency_key = stripe_request.idempotency_key or ""

        return self.create(
            stripe_id=event.id,
            mode=mode,
            state=WebhookEvent.State.RECEIVED,
            event_type=event.type,
            data=event.data.object,
            api_version=event.api_version,
            stripe_created_at=stripe_created_at,
            request_id=request_id,
            request_idempotency_key=request_idempotency_key,
            headers=dict(request.headers),
            remote_ip=remote_ip,
        )


class WebhookEvent(StripeModel):
    """
    Models a single Stripe event received via the webhook.

    See https://stripe.com/docs/api/events/object

    Only webhook events with valid payloads & validated Stripe
    header signatures are stored.

    State: RECEIVED
    ---------------

    The webhook event has been received, and returned a success
    response to stripe - but no handlers were registered against
    the event type and thus no actual processing occurred.


    State: PROCESSED
    ----------------

    The webhook event has been received, and returned a success
    response to stripe, and was successfully processed by at least
    one registered handler.
    """

    class State(models.TextChoices):
        RECEIVED = ("RECEIVED", _("Received"))
        PROCESSED = ("PROCESSED", _("Processed"))

    state = models.CharField(
        max_length=20, choices=State.choices, default=State.RECEIVED
    )

    # Event-object related fields.
    event_type = models.CharField(max_length=100)
    data = JSONField(
        help_text=_(
            "The contents of data.object, representing the object "
            "the webhook event was triggered for."
        )
    )
    api_version = models.CharField(max_length=40)
    stripe_created_at = models.DateTimeField()

    # Instigating request related fields.
    request_id = models.CharField(max_length=255, blank=True)
    request_idempotency_key = models.CharField(max_length=255, blank=True)

    # Inbound webhook request data that we store
    # for security monitoring purposes only.
    headers = JSONField(blank=True)
    remote_ip = models.GenericIPAddressField(
        verbose_name=_("Remote IP"), help_text=_("IP address of the remote client.")
    )

    objects = WebhookEventManager.from_queryset(WebhookEventQuerySet)()

    def __str__(self) -> str:
        return f"WebhookEvent: {self.stripe_id}"

    def __repr__(self) -> str:
        return "<WebhookEvent id={} stripe_id={} mode={} state={}>".format(
            self.id, self.stripe_id, self.mode, self.state
        )

    @property
    def is_processed(self) -> bool:
        return self.state == self.State.PROCESSED

    def mark_processed(self) -> None:
        if self.is_processed:
            raise ValueError("You may not re-process a processed WebhookEvent")
        self.state = self.State.PROCESSED
