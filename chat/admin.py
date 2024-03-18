from django.contrib import admin
from .models import ChatRoom
from .forms import ChatRoomForm

# 어드민 페이지를 통해 ChatRoom을 생성/조회/수정/삭제할 수 있다.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    form = ChatRoomForm

    def save_model(self, request, obj, form, change):
        if change is False and form.is_valid(): # change 인자는 bool 타입으로 신규 생성 여부를 뜻한다. False면 신규 생성.
            obj.user = request.user
        super().save_model(request, obj, form, change)

