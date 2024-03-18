from django.contrib.admin.views.decorators import staff_member_required
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from gtts import gTTS

from .models import ChatRoom
from .forms import ChatRoomForm

@method_decorator(staff_member_required, name='dispatch')
class ChatRoomListView(ListView):
    model = ChatRoom

    # 사용자가 생성한 채팅방만 조회
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) # 현재 로그인한 유저가 생성한 채팅방만 조회
        return qs

    # json으로 qs 변환 후 JsonResponse 반환.
    def render_to_response(self, context, **response_kwargs):
        data = [model_to_dict(chatroom) for chatroom in context['object_list']]
        return JsonResponse(data, safe=False)

chat_room_list = ChatRoomListView.as_view()

#DetailView를 상속받는 ChatRoomDetailView 클래스를 새롭게 정의
@method_decorator(staff_member_required, name='dispatch')
class ChatRoomDetailView(DetailView):
    model = ChatRoom

    # 사용자가 생성한 채팅방만 조회
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user) # 현재 로그인한 유저가 생성한 채팅방만 조회
        return qs

chat_room_detail = ChatRoomDetailView.as_view()

#ChatRoom 생성
#CreateView를 상속받는 RolePlayingRoomCreateView 클래스를 새롭게 정의
@method_decorator(staff_member_required, name='dispatch')
class ChatRoomCreateView(CreateView):
    model = ChatRoom
    form_class = ChatRoomForm

    # 유저 입력요청에 대한 유효성 검사가 통과했을 때, form_valid 메서드 호출
    def form_valid(self, form):

        #instance.save() 호출 전, user필드 할당.
        chat_room = form.save(commit=False)
        chat_room.user = self.request.user

        data = {
            'success': True,
            'message': 'ChatRoom created successfully',
            'ChatRoom_id': self.object.id
        }

        return JsonResponse(data)


# ChatRoomCreateView 클래스를 뷰 함수로 변환하여 chat_room_new 변수에 할당.
# 이렇게 함으로써 뷰를 URL 패턴에 매핑할 때 사용할 수 있다.
chat_room_new = ChatRoomCreateView.as_view()

@method_decorator(staff_member_required, name="dispatch")
class ChatRoomDeleteView(DeleteView):
    model = ChatRoom # 삭제 대상 모델 지정

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {
            'success': True,
            'message': 'ChatRoom deleted successfully'
        }
        return JsonResponse(data)

chat_room_delete = ChatRoomDeleteView.as_view()

# mp3 파일 생성해 반환.
@staff_member_required
def make_voice(request):
    # lang 이라는 쿼리 매개변수의 값을 가져오는데 없으면 기본값으로 en 사용.
    lang = request.GET.get("lang", "en")
    message = request.GET.get("message")

    response = HttpResponse()

    gTTS(message, lang=lang).write_to_fp(response)
    response["Content-Type"] = "audio/mpeg"

    return response
