from collections import defaultdict
from unittest import mock

from django_stripe import webhooks
from django_stripe.models import WebhookEvent


def test_function_to_wrap():
    pass


def test_function_to_wrap2():
    pass


class TestStripeWebhookHandler:
    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_single_event_handler(self):
        webhooks.stripe_webhook_handler("full.event.type")(test_function_to_wrap)
        assert dict(webhooks.REGISTRY) == {"full.event.type": [test_function_to_wrap]}

    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_single_event_handler_with_multiple_events(self):
        webhooks.stripe_webhook_handler("full.event.type1", "full.event.type2")(
            test_function_to_wrap
        )
        assert dict(webhooks.REGISTRY) == {
            "full.event.type1": [test_function_to_wrap],
            "full.event.type2": [test_function_to_wrap],
        }

    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_multiple_event_handlers_with_single_event(self):
        webhooks.stripe_webhook_handler("full.event.type")(test_function_to_wrap)
        webhooks.stripe_webhook_handler("full.event.type")(test_function_to_wrap2)
        assert dict(webhooks.REGISTRY) == {
            "full.event.type": [test_function_to_wrap, test_function_to_wrap2]
        }

    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_multiple_event_handlers_with_multiple_events(self):
        webhooks.stripe_webhook_handler("full.event.type1", "full.event.type2")(
            test_function_to_wrap
        )
        webhooks.stripe_webhook_handler("full.event.type1", "full.event.type2")(
            test_function_to_wrap2
        )
        assert dict(webhooks.REGISTRY) == {
            "full.event.type1": [test_function_to_wrap, test_function_to_wrap2],
            "full.event.type2": [test_function_to_wrap, test_function_to_wrap2],
        }


class TestRunHandlers:
    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_with_handlers_registered_for_event(self):
        function_1 = mock.Mock()
        function_2 = mock.Mock()
        webhooks.stripe_webhook_handler("full.event.type")(function_1)
        webhooks.stripe_webhook_handler("full.event.type")(function_2)

        event = mock.Mock(spec=WebhookEvent)
        event.event_type = "full.event.type"
        webhooks.run_handlers(event)

        function_1.assert_called_once_with(event=event)
        function_2.assert_called_once_with(event=event)

        event.mark_processed.assert_called_once_with()
        event.save.assert_called_once_with(
            update_fields=["state", "db_last_updated_at"]
        )

    @mock.patch.object(webhooks, "REGISTRY", defaultdict(list))
    def test_with_no_handlers_registered_for_event(self):
        event = mock.Mock(spec=WebhookEvent)
        event.event_type = "full.event.type"
        webhooks.run_handlers(event)

        event.mark_processed.assert_not_called()
        event.save.assert_not_called()
