from __future__ import annotations

from typing import Any

from django.db import models


class StripeIdField(models.CharField):
    """Represent an identifier in Stripe format."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Provide sane defaults for fields storing Stripe IDs.

        See: https://stripe.com/docs/upgrades

        "You can safely assume object IDs we generate will
        never exceed 255 characters, but you should be able
        to handle IDs of up to that length."
        """
        defaults = {"max_length": 255, "blank": False, "null": False, "unique": True}
        defaults.update(kwargs)
        super().__init__(*args, **defaults)
