import redis
from django.conf import settings
from django.contrib.auth import get_user_model

from notifications.models import Notification
from .websocket_backend import WebSocketBackend
from .email_backend import EmailBackend
from .sms_backend import SMSBackend

User = get_user_model()


class NotificationDispatcher:
    def __init__(self):
        self.ws_backend = WebSocketBackend()
        self.email_backend = EmailBackend()
        self.sms_backend = SMSBackend()
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)

    def _is_user_online(self, user_id: int) -> bool:
        return bool(self.redis_client.sismember("online-users", user_id))

    def _fallback_channels(self, user):
        """
        Decide fallback order: email first, then SMS.
        You can make this configurable per user.
        """
        fallbacks = []
        if getattr(user, "email", None):
            fallbacks.append("email")

        phone = getattr(getattr(user, "profile", None), "phone", None)
        if phone:
            fallbacks.append("sms")

        return fallbacks, phone if fallbacks and "sms" in fallbacks else None

    def dispatch(self, notification_id: int):
        notification = Notification.objects.select_related("user").get(pk=notification_id)
        user = notification.user

        payload = {
            "id": notification.id,
            "title": notification.title,
            "body": notification.body,
            "data": notification.data,
            "created_at": notification.created_at.isoformat(),
        }

        sent = False

        # Primary channel
        if notification.channel == Notification.CHANNEL_WEBSOCKET:
            online = self._is_user_online(user.id)
            if online:
                self.ws_backend.send(user.id, payload)
                sent = True
            else:
                # Fallback if offline
                fallbacks, phone = self._fallback_channels(user)
                for ch in fallbacks:
                    if ch == "email":
                        self.email_backend.send(user.email, notification.title, notification.body)
                        sent = True
                    elif ch == "sms" and phone:
                        self.sms_backend.send(phone, notification.body)
                        sent = True

        elif notification.channel == Notification.CHANNEL_EMAIL:
            if user.email:
                self.email_backend.send(user.email, notification.title, notification.body)
                sent = True

        elif notification.channel == Notification.CHANNEL_SMS:
            phone = getattr(getattr(user, "profile", None), "phone", None)
            if phone:
                self.sms_backend.send(phone, notification.body)
                sent = True

        # Mark as sent if any channel succeeded (basic implementation)
        if sent and not notification.sent_at:
            notification.sent_at = notification.created_at
            notification.save(update_fields=["sent_at"])