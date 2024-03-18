from typing import List

import openai
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import AbstractUser

from chat.models import ChatRoom, GptMessage


class ChatRoomConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수
        self.gpt_messages: List[GptMessage] = []
        self.recommend_message: str = ""

    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            # 웹소켓 연결시에 gpt_messages, recommend_message 미리 할당받기.
            self.gpt_messages = room.get_initial_messages()
            self.recommend_message = room.get_recommend_message()

            assistant_message = self.get_query()
            self.send_json({
                "type": "assistant-message",
                "message": assistant_message,
            })

    # 웹 소켓 클라이언트로부터 메세지 값을 받을 때 마다 호출
    def receive_json(self, content_dict, **kwargs):
        if content_dict["type"] == "user-message":
            assistant_message = self.get_query(user_query=content_dict["message"])
            self.send_json({
                "type": "assistant-message",
                "message": assistant_message,
            })
        else:
            self.send_json({
                "type": "error",
                "message": f"Invalid type: {content_dict['type']}",
            })

    # 조회에 실패하면 예외발생없이 None 반환.
    def get_room(self) -> ChatRoom | None:
        user: AbstractUser = self.scope['user']
        room_pk = self.scope['url_route']['kwargs']['room_pk']
        room: ChatRoom = None

        # 유저가 인증되어있다면
        if user.is_authenticated:
            try:
                room = ChatRoom.objects.get(pk=room_pk, user=user)  # 조회 조건으로 room_pk와 user 지정
            except ChatRoom.DoesNotExist:  # 해당 room 못찾을 경우 예외발생
                pass

        return room

    # command_query : 표현 추천받기..., user_query : 사용자 query
    def get_query(self, user_query: str = None) -> str:
        if user_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=user_query))
        else:
            raise ValueError("user_query는 None이 될 수 없습니다.")

        response_dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_messages,
            temperature=1,  # 무작위성 최대한 높임
        )

        # gpt 응답에서 role, content 내용 가져오기
        response_role = response_dict["choices"][0]["message"]["role"]  # 응답에서 role은 assistant가 될 것.
        response_content = response_dict["choices"][0]["message"]["content"]

        # 일반 프리토킹일 경우 대화 내역 기록 남기기
        gpt_messages = GptMessage(role=response_role, content=response_content)
        self.gpt_messages.append(gpt_messages),

        return response_content
