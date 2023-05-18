import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'].username
        self.room_group_name = 'global'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                "user": self.user,
                "message": message
            }
        )
    def chat_message(self,event):
        message = event['message']
        user = event["user"]
        self.send(text_data=json.dumps({
            'type':'chat',
            "user":user,
            "message": message
        }))


class OneonOneChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'].username
        # self.room_group_name = 'global'
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        # self.accept()
        current_user_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        self.room_name = (
            f'{current_user_id}_{other_user_id}'
            if int(current_user_id) > int(other_user_id)
            else f'{other_user_id}_{current_user_id}'
        )
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)


    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                "user": self.user,
                "message": message
            }
        )
    def chat_message(self,event):
        message = event['message']
        user = event["user"]
        self.send(text_data=json.dumps({
            'type':'chat',
            "user":user,
            "message": message
        }))

