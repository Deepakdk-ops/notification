from django.urls import re_path
from .consumers import UserNotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<user_id>\d+)/$", UserNotificationConsumer.as_asgi()),
]