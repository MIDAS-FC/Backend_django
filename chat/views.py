import openai
from django.http import HttpResponse, JsonResponse
from gtts import gTTS


# mp3 파일 생성해 반환.
def make_voice(request):
    # lang 이라는 쿼리 매개변수의 값을 가져오는데 없으면 기본값으로 en 사용.
    lang = request.GET.get("lang", "en")
    message = request.GET.get("message")

    response = HttpResponse()

    gTTS(message, lang=lang).write_to_fp(response)
    response["Content-Type"] = "audio/mpeg"

    return response


# 오디오 파일 받아서 STT 수행
def make_text(request):
    audio = request.FILES['audio']

    text = openai.Audio.transcribe(model="whisper-1", file=audio)

    return JsonResponse(text)
