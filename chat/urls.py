from django.urls import path
from . import views

urlpatterns = [
    # STT
    path('stt/', views.make_text, name='make_text'),
    # 음성 mp3 생성
    path("voice/", views.make_voice, name="make_voice")
]