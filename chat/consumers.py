import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'].username
        print(self.user)
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