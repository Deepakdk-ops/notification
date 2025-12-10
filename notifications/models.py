from django.conf import settings
from django.db import models


class Notification(models.Model):
    CHANNEL_WEBSOCKET = "websocket"
    CHANNEL_EMAIL = "email"
    CHANNEL_SMS = "sms"

    CHANNEL_CHOICES = [
        (CHANNEL_WEBSOCKET, "WebSocket"),
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_SMS, "SMS"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_index=True,
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    channel = models.CharField(
        max_length=32, choices=CHANNEL_CHOICES, default=CHANNEL_WEBSOCKET
    )
    data = models.JSONField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.title} ({self.channel})"