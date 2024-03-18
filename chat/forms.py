from django import forms
from chat.models import ChatRoom

# ModelForm은 ChatRoom 모델 기반
class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        # 모든 RolePlayingRoom 모델 필드 내역들을 다 읽어와서 자동으로 Form fields 생성.
        # 유저에게 제공할 HTML 입력 필드들을 Form 클래스가 생성도 해주고, 유효성 검사도 수행.
        # 입력받아야 하는 필드 설정.
        fields = [
            "language",
            "level",
            "situation",
        ]

    # clean 메서드 재정의를 통해, 폼 필드 다수에 대한 유효성 검사를 수행할 수 있고, 값의 변환도 할 수 있다.
    # def clean(self):
    #     situation = self.cleaned_data.get("situation")
    #
    #     return self.cleaned_data

