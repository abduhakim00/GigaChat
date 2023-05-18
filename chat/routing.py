from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path('ws/socket-server/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:id>/', consumers.OneonOneChatConsumer.as_asgi()),
]