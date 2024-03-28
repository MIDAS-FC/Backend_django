import openai
from django.http import HttpResponse, JsonResponse
from gtts import gTTS


# mp3 파일 생성해 반환.
def make_voice(request):
    lang = request.GET.get("lang")
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
