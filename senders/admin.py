from django.contrib import admin

from senders.models import MailAttemptToSend, Mailing, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "comment",
        "owner",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "middle_name",
    )
    list_filter = ("first_name", "last_name")
    ordering = ("first_name", "last_name")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "comment",
                    "owner",
                )
            },
        ),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject",)
    ordering = ("subject",)
    fieldsets = ((None, {"fields": ("subject", "body", "owner")}),)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "start_date",
        "end_date",
        "status",
        "message",
        "owner",
    )
    search_fields = (
        "status",
        "sender__first_name",
        "sender__last_name",
    )
    list_filter = ("status",)
    ordering = ("start_date",)
    filter_horizontal = ("recipients",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "status",
                    "message",
                    "recipients",
                    "owner",
                )
            },
        ),
    )


@admin.register(MailAttemptToSend)
class MailAttemptToSendAdmin(admin.ModelAdmin):
    list_display = (
        "mailing",
        "attempt_date",
        "status",
        "server_response",
    )
    search_fields = (
        "mailing__message__subject",
        "status",
        "server_response",
    )
    list_filter = ("status",)
    ordering = ("-attempt_date",)
    readonly_fields = ("attempt_date",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "mailing",
                    "attempt_date",
                    "status",
                    "server_response",
                )
            },
        ),
    )
