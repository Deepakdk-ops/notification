from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NotificationCreateSerializer
from notifications.tasks import dispatch_notification_task


class NotificationTriggerView(APIView):
    """
    POST /api/notifications/trigger/
    {
        "user": 1,
        "title": "Order Placed",
        "body": "Your order #1234 has been placed",
        "channel": "websocket",  # or "email", "sms"
        "data": {"order_id": 1234}
    }
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()

        # Async processing
        dispatch_notification_task.delay(notification.id)

        return Response(
            {"id": notification.id, "status": "queued"},
            status=status.HTTP_201_CREATED,
        )