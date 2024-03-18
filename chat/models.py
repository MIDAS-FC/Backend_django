from typing import List, TypedDict, Literal

from django.db import models
from django.conf import settings
from django.urls import reverse


class GptMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRoom(models.Model):
    # 왼-데이터베이스에 저장되는 필드명, 오-유저에게 보여지는 값
    class Language(models.TextChoices):
        ENGLISH = "en-US", "English"
        JAPANESE = "ja-JP", "Japanese"
        CHINESE = "zh-CN", "Chinese"
        KOREAN = "ko-KR", "Korean"

    class EnglishLevel(models.IntegerChoices):
        A1 = 1, "입문"
        A2 = 2, "초급"
        B1 = 3, "중급"
        B2 = 4, "중상급"
        C1 = 5, "상급"
        C2 = 6, "고급"

    class Level(models.IntegerChoices):
        BEGINNER = 1, "초급"
        ADVANCED = 2, "고급"

    # 이 모델로 부터 파생되는 QuerySet에 디폴트 정렬 방향을 지정.
    # 디폴트 정렬 방향은 "기본 키에 대한 역순 정렬"
    class Meta:
        ordering = ["-pk"]

    # 각 유저는 저마다의 새로운 상황극 채팅방을 만들 수 있어야 되겠기에, 생성한 유저를 기록하는 User 모델을 외래키 필드로서 user 필드를 추가한다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 대화 언어를 저장할 language 필드 추가
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.ENGLISH,
        verbose_name="대화 언어"
    )

    if language == Language.ENGLISH:
        level = models.SmallIntegerField(
            choices=EnglishLevel.choices,
            default=EnglishLevel.A1,
            verbose_name="영어 레벨"
        )
    else:
        # 대화 레벨을 저장할 level 필드 추가 1-초급, 2-고급
        level = models.SmallIntegerField(
            choices=Level.choices,
            default=Level.BEGINNER,
            verbose_name="레벨"
        )

    # 상황을 저장할 situation 필드 추가. 최대 100개 문자 허용
    situation = models.CharField(max_length=100, verbose_name="상황")

    # def get_absolute_url(self) -> str:
    #     return reverse("role_playing_room_detail", args=[self.pk])
    #
    # def get_initial_messages(self) -> List[GptMessage]:
    #     gpt_name = "RolePlayingBot"
    #     language = self.get_language_display()
    #     situation_en = self.situation_en
    #     my_role_en = self.my_role_en
    #     gpt_role_en = self.gpt_role_en
    #
    #     if self.level == self.Level.BEGINNER:
    #         level_string = f"a beginner in {language}"
    #         level_word = "simple"
    #     elif self.level == self.Level.ADVANCED:
    #         level_string = f"a advanced in {language}"
    #         level_word = "advanced"
    #     else:  # level 구체적으로 정해지면 elif 추가
    #         raise ValueError(f"Invalid level : {self.level}")
    #
    #     system_message = (
    #         f"You are helpful assistant supporting people learning {language}. "
    #         f"Your name is {gpt_name}. "
    #         f"Please assume that the user you are assisting is {level_string}. "
    #         f"And please write only the sentence without the character role."
    #
    #     )
    #
    #     user_message = (
    #         f"Let's have a conversation in {language}. "
    #         f"Please answer in {language} only "
    #         f"without providing a translation. "
    #         f"And please don't write down the pronunciation either. "
    #         f"Let us assume that the situation in '{situation_en}'. "
    #         f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    #         f"Please make sure that I'm {level_string}, so please use {level_word} words "
    #         f"as much as possible. Now, start a conversation with the first sentence!"
    #     )
    #
    #     return [
    #         GptMessage(role="system", content=system_message),
    #         GptMessage(role="user", content=user_message),
    #     ]
    #
    # def get_recommend_message(self) -> str:
    #
    #     if self.level == self.Level.BEGINNER:
    #         level_word = "simple"
    #     elif self.level == self.Level.ADVANCED:
    #         level_word = "advanced"
    #     else:
    #         raise ValueError(f"Invalid level : {self.level}")
    #     return (
    #         f"Can you please provide me an {level_word} example "
    #         f"of how to respond to the last sentence "
    #         f"in this situation, without providing a translation "
    #         f"and any introductory phrases or sentences."
    #     )
