from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/aichat/<int:room_pk>/", consumers.ChatRoomConsumer.as_asgi())
]