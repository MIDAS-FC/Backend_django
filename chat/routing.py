from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/aichat/", consumers.ChatConsumer.as_asgi())
]