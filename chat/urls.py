from django.urls import path
from . import views

urlpatterns = [
    # 채팅방 생성
    path("aichat/new/", views.chat_room_new, name="chat_room_new"),
    # 채팅방 목록
    path("aichat/list/", views.chat_room_list, name="chat_room_list"),
    # 채팅방 입장
    path("aichat/<int:pk>/", views.chat_room_detail, name="chat_room_detail"),
    # 채팅방 삭제
    path("aichat/<int:pk>/delete/", views.chat_room_delete, name="chat_room_delete"),
    # 음성 mp3 생성
    path("voice/", views.make_voice, name="make_voice")
]