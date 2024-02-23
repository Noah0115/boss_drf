from django.urls import re_path
from back import consumers

websocket_urlpatterns = [
    re_path(r'test/', consumers.ChatConsumer.as_asgi())
]