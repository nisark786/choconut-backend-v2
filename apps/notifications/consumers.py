import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Personal room for the user
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            
            # If admin, also join admin group
            if self.user.is_staff:
                await self.channel_layer.group_add("admins", self.channel_name)
            
            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            if self.user.is_staff:
                await self.channel_layer.group_discard("admins", self.channel_name)

    async def send_notification(self, event):
        # Sends the actual data to React
        await self.send(text_data=json.dumps(event["payload"]))