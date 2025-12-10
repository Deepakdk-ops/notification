from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketBackend:
    def __init__(self):
        self.channel_layer = get_channel_layer()

    def send(self, user_id: int, payload: dict):
        group_name = f"user-notifications-{user_id}"
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                "type": "notify",
                "payload": payload,
            },
        )