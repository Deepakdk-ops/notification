import json
import redis
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

# Use the same REDIS_URL from settings
redis_client = redis.Redis.from_url(settings.REDIS_URL)


class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user-notifications-{self.user_id}"

        # Mark user as online in Redis
        redis_client.sadd("online-users", self.user_id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        redis_client.srem("online-users", self.user_id)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["payload"]))