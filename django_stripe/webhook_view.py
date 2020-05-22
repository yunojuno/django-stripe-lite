from __future__ import annotations

import logging

import stripe
from django.db import transaction
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import settings, webhooks
from .models import WebhookEvent

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
@transaction.atomic
def webhook_view(request: HttpRequest) -> HttpResponse:
    """
    Handle inbound Stripe webhook events.

    This endpoint is open to the web, but we only accept requests
    that have a valid signature from Stripe themselves, based on
    our WEBHOOK_SECRET.

    Successly received => HTTP 200
    Invalid payload (as deemed by Stripe library) => HTTP 400
    Invalid/missing signature => HTTP 403
    Unhandled exception => HTTP 500

    Anything but an HTTP 200 response to Stripe will result in
    Stripe replaying the webhook at a later date. If the failures
    continue, Stripe will eventually put the webhook in the errored
    state and stop sending events.
    """
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.headers.get("Stripe-Signature"),
            settings.WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponseForbidden("Invalid signature")
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")

    persisted_event = WebhookEvent.objects.create_from_event(request, event)
    webhooks.run_handlers(persisted_event)
    return HttpResponse(persisted_event.id, status=200)
