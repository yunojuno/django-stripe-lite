# Generated by Django 3.0.6 on 2020-05-21 14:00

import django.contrib.postgres.fields.jsonb
import django_stripe.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WebhookEvent",
            fields=[
                (
                    "db_created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Database created at"
                    ),
                ),
                (
                    "db_last_updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Database last updated at"
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "stripe_id",
                    django_stripe.db.fields.StripeIdField(max_length=255, unique=True),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[("LIVE", "Live"), ("TEST", "Test")], max_length=20
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[("RECEIVED", "Received"), ("PROCESSED", "Processed")],
                        default="RECEIVED",
                        max_length=20,
                    ),
                ),
                ("event_type", models.CharField(max_length=100)),
                (
                    "data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        help_text=(
                            "The contents of data.object, representing the object the "
                            "webhook event was triggered for."
                        )
                    ),
                ),
                ("api_version", models.CharField(max_length=40)),
                ("stripe_created_at", models.DateTimeField()),
                ("request_id", models.CharField(blank=True, max_length=255)),
                (
                    "request_idempotency_key",
                    models.CharField(blank=True, max_length=255),
                ),
                ("headers", django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                (
                    "remote_ip",
                    models.GenericIPAddressField(
                        help_text="IP address of the remote client.",
                        verbose_name="Remote IP",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
