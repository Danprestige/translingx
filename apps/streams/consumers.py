import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.translations.engine import translate_text


class TranslationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room = self.scope["url_route"]["kwargs"]["room"]

        self.group = f"room_{self.room}"

        await self.channel_layer.group_add(self.group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):

        data = json.loads(text_data)

        text = data["text"]

        language = data["language"]

        translated = translate_text(text, language)

        await self.channel_layer.group_send(
            self.group,
            {
                "type": "chat_message",
                "message": translated
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))