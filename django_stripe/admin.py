from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import WebhookEvent


class WebhookEventAdmin(admin.ModelAdmin):
    date_hierarchy = "stripe_created_at"
    list_display = (
        "stripe_id",
        "event_type",
        "state",
        "mode",
        "api_version",
        "remote_ip",
        "stripe_created_at",
        "db_created_at",
    )
    list_filter = ("state", "mode", "api_version", "event_type")
    fieldsets = (
        (None, {"fields": ("stripe_id", "event_type", "mode", "state")}),
        (
            _("Webhook Payload"),
            {"fields": ("data", "api_version", "stripe_created_at")},
        ),
        (
            _("Instigating Request Details"),
            {"fields": ("request_id", "request_idempotency_key")},
        ),
        (_("Webhook Request Details"), {"fields": ("headers", "remote_ip")}),
        (_("Database Timestamps"), {"fields": ("db_created_at", "db_last_updated_at")}),
    )
    readonly_fields = ("db_created_at", "db_last_updated_at")
    search_fields = ("event_type",)
    ordering = ("-db_created_at",)


admin.site.register(WebhookEvent, WebhookEventAdmin)
