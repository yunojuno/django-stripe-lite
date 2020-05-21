from __future__ import annotations

import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..db.fields import StripeIdField

logger = logging.getLogger(__name__)


class TimestampedModel(models.Model):
    db_created_at = models.DateTimeField(_("Database created at"), auto_now_add=True)
    db_last_updated_at = models.DateTimeField(
        _("Database last updated at"), auto_now=True
    )

    class Meta:
        abstract = True


class StripeModel(TimestampedModel):
    """Provide base functionality for all Stripe-object models."""

    class Mode(models.TextChoices):
        LIVE = ("LIVE", _("Live"))
        TEST = ("TEST", _("Test"))

        @classmethod
        def from_stripe_livemode(cls, livemode: bool) -> StripeModel.Mode:
            return cls.LIVE if livemode else cls.TEST  # type: ignore

    id = models.BigAutoField(primary_key=True)
    stripe_id = StripeIdField()

    mode = models.CharField(max_length=20, choices=Mode.choices)

    class Meta:
        abstract = True

    @property
    def is_live_mode(self) -> bool:
        return self.mode == self.Mode.LIVE

    @property
    def is_test_mode(self) -> bool:
        return self.mode == self.Mode.TEST
