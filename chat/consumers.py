from typing import List

import openai
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import GptMessage


class ChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수
        self.gpt_messages: List[GptMessage] = []

    def connect(self):
        self.accept()

    # 웹 소켓 클라이언트로부터 메세지 값을 받을 때 마다 호출
    def receive_json(self, content_dict, **kwargs):
        if content_dict["type"] == "user-message":
            assistant_message = self.get_query(user_query=content_dict["message"]).split("&")
            self.send_json({
                "type": "assistant-message",
                "message": assistant_message[0],
                "translate": assistant_message[1],
            })
        elif content_dict["type"] == "set-data":
            self.set_data(level=content_dict["level"], user_lang=content_dict["userLang"],
                          chat_lang=content_dict["chatLang"])
            self.send_json({
                "type": "success",
                "message": f"설정 변경 성공"
            })
        elif content_dict["type"] == "init-data":
            assistant_message = self.init_data(level=content_dict["level"], user_lang=content_dict["userLang"],
                                               chat_lang=content_dict["chatLang"]).split("&")
            self.send_json({
                "type": "assistant-message",
                "message": assistant_message[0],
                "translate": assistant_message[1],
            })
        else:
            self.send_json({
                "type": "error",
                "message": f"Invalid type: {content_dict['type']}",
            })

    # user_query : 사용자 query
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

    # 웹소켓 연결 직후
    def init_data(self, level: str = None, user_lang: str = None, chat_lang: str = None) -> str:

        if level is not None and user_lang is not None and chat_lang is not None:

            system_message = (
                f"You are helpful assistant supporting people learning {chat_lang}. "
                f"Your name is ChatBot."
                f"Please assume that the user you are assisting is {level} in {chat_lang}. "
                f"And please write only the sentence without the character role."
            )

            # 사용하는 단어의 난이도 조정 추가하기
            user_message = (
                f"Let's have a conversation in {chat_lang}. "
                f"Please answer in {chat_lang} only and provide {user_lang} translation. "
                f"Also please don't write down the pronunciation "
                f"Please make sure that I'm {level} in {chat_lang} "
                f"Please use '&' to separate {chat_lang} responses and {user_lang} translations. "
                f"For example, {chat_lang}&{user_lang} "
                f"Now, start a conversation with the first sentence!"
            )

            self.gpt_messages.append(GptMessage(role="system", content=system_message))

            response_content = self.get_query(user_query=user_message)

            return response_content
        else:
            raise ValueError("level, user_lang, chat_lang 중 None인 값이 있습니다.")

    # 사용자가 level, lang 바꿨을 때
    def set_data(self, level: str = None, user_lang: str = None, chat_lang: str = None) -> None:
        if level is not None and user_lang is not None and chat_lang is not None:

            system_message = (
                f"You are helpful assistant supporting people learning {chat_lang}. "
                f"Your name is ChatBot."
                f"Please assume that the user you are assisting is {level} in {chat_lang}. "
                f"And please write only the sentence without the character role."
            )

            # 사용하는 단어의 난이도 조정 추가하기
            user_message = (
                f"Let's change the language of the conversation to {chat_lang}. "
                f"Please answer in {chat_lang} only and provide {user_lang} translation. "
                f"Also please don't write down the pronunciation "
                f"Please make sure that I'm {level} in {chat_lang} "
                f"Please use '&' to separate {chat_lang} responses and {user_lang} translations. "
                f"For example, {chat_lang}&{user_lang} "
                f"Let's continue the previous conversation. "
                f"I'll start. "
            )

            self.gpt_messages.append(GptMessage(role="system", content=system_message))

            response_content = self.get_query(user_query=user_message)
        else:
            raise ValueError("level, user_lang, chat_lang 중 None인 값이 있습니다.")
