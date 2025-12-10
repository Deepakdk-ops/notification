from rest_framework import serializers
from notifications.models import Notification


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user", "title", "body", "channel", "data"]