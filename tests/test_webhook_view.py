import json
import time
from unittest import mock

import pytest
from django_stripe import settings, stripe, webhooks
from django_stripe.models import WebhookEvent


def generate_dummy_payload():
    return {
        "api_version": "2020-03-02",
        "created": int(time.time()),
        "data": {
            "object": {
                "application": None,
                "cancellation_reason": None,
                "client_secret": "seti_1GlJj7CAR2OHHViIkChgDTxZ_secret_HJxe5hFYmA05h82ZkOORWX4b0GQZx7y",
                "created": 1590088005,
                "customer": None,
                "description": "(created by Stripe CLI)",
                "id": "seti_1GlJj7CAR2OHHViIkChgDTxZ",
                "last_setup_error": None,
                "livemode": False,
                "mandate": None,
                "metadata": {},
                "next_action": None,
                "object": "setup_intent",
                "on_behalf_of": None,
                "payment_method": None,
                "payment_method_options": {
                    "card": {"request_three_d_secure": "automatic"}
                },
                "payment_method_types": ["card"],
                "single_use_mandate": None,
                "status": "requires_payment_method",
                "usage": "off_session",
            }
        },
        "id": "evt_1GlJj7CAR2OHHViIPHqLxw8g",
        "livemode": False,
        "object": "event",
        "pending_webhooks": 2,
        "request": {"id": "req_JJ8xGpqam5TM8V", "idempotency_key": None},
        "type": "setup_intent.created",
    }


def _generate_signature_header(timestamp: int, payload: str):
    # We could mock this, but for an integration test I want it
    # to actually generate a valid signature for a valid payload
    # and have that signature verified by the actual view.
    scheme = stripe.WebhookSignature.EXPECTED_SCHEME
    payload_to_sign = "%d.%s" % (timestamp, payload)
    signature = stripe.WebhookSignature._compute_signature(
        payload_to_sign, settings.WEBHOOK_SECRET
    )
    return "t=%d,%s=%s" % (timestamp, scheme, signature)


@pytest.mark.django_db
def test_webhook_view__handles_event(client):
    """
    An integration test to cover the sending, storing
    and processing of a Stripe inbound webhook payload.
    """
    payload_dict = generate_dummy_payload()
    payload = json.dumps(payload_dict)
    signature = _generate_signature_header(
        timestamp=payload_dict["created"], payload=payload
    )

    # Register a single handler against the event type.
    mock_handler = mock.Mock()
    webhooks.stripe_webhook_handler(payload_dict["type"])(mock_handler)

    assert not WebhookEvent.objects.exists()

    response = client.post(
        "/stripe/webhook/",
        payload_dict,
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE=signature,
        HTTP_SOME_RANDOM_HEADER="for-testing",
        HTTP_X_FORWARDED_FOR="172.18.0.1",
    )

    assert response.status_code == 200

    webhook_event = WebhookEvent.objects.get(id=response.content)
    assert WebhookEvent.objects.count() == 1

    assert webhook_event.stripe_id == payload_dict["id"]
    assert webhook_event.mode == WebhookEvent.Mode.TEST
    assert webhook_event.is_live_mode is False
    assert webhook_event.is_test_mode is True

    # The state should be processed, as one handler was registered
    # and should have completed successfully as it was no-op.
    assert webhook_event.state == WebhookEvent.State.PROCESSED
    assert webhook_event.is_processed

    assert webhook_event.api_version == payload_dict["api_version"]
    assert webhook_event.event_type == payload_dict["type"]
    assert webhook_event.data == payload_dict["data"]["object"]
    assert webhook_event.request_id == payload_dict["request"]["id"]
    assert webhook_event.request_idempotency_key == ""
    assert webhook_event.headers["Stripe-Signature"] == signature
    assert webhook_event.headers["Some-Random-Header"] == "for-testing"
    assert webhook_event.headers["X-Forwarded-For"] == "172.18.0.1"
    assert webhook_event.remote_ip == "172.18.0.1"

    # Assert the handler registered was called once with the event.
    mock_handler.assert_called_once_with(event=webhook_event)


@pytest.mark.django_db
def test_webhook_view__returns_403_for_bad_signature(client):
    payload_dict = generate_dummy_payload()

    # Register a single handler against the event type,
    # so that we can later ensure it was not called.
    mock_handler = mock.Mock()
    webhooks.stripe_webhook_handler(payload_dict["type"])(mock_handler)

    assert not WebhookEvent.objects.exists()

    response = client.post(
        "/stripe/webhook/",
        payload_dict,
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="bad signature",
    )

    assert response.status_code == 403
    assert response.content == b"Invalid signature"

    # Assert the handler registered was not called
    # and that the event was not persisted.
    mock_handler.assert_not_called()
    assert not WebhookEvent.objects.exists()
