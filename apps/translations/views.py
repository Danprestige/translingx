from rest_framework.views import APIView
from rest_framework.response import Response
from .engine import translate_text

class TranslateAPI(APIView):

    def post(self, request):

        text = request.data["text"]

        lang = request.data["language"]

        translated = translate_text(text, lang)

        return Response({
            "translated": translated
        })