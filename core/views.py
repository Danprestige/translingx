# core/views.py
import speech_recognition as sr
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from deep_translator import GoogleTranslator

from .models import User, Post
from .serializers import UserSerializer, PostSerializer

# ----------------------
# User API
# ----------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can manage users

# ----------------------
# Post API
# ----------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can create/update posts
    parser_classes = [MultiPartParser, FormParser]  # for file uploads

    # Optional: Translate a post on demand
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def translate(self, request, pk=None):
        """
        Translate a post content to the requested language
        Example: GET /api/posts/1/translate/?lang=fr
        """
        post = self.get_object()
        target_lang = request.query_params.get('lang', 'en')  # default English
        translated_content = GoogleTranslator(source='auto', target=target_lang).translate(post.content)
        return Response({
            'original': post.content,
            'translated': translated_content,
            'target_language': target_lang
        })

    # ----------------------
    # Speech-to-Text Endpoint
    # ----------------------
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def speech_to_text(self, request, pk=None):
        """
        Upload an audio file to convert to text
        Example: POST /api/posts/1/speech_to_text/
        Form-Data: audio_file=<file>
        """
        post = self.get_object()
        audio = request.FILES.get('audio_file')
        if not audio:
            return Response({'error': 'No audio file provided'}, status=400)

        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
        except Exception as e:
            return Response({'error': f'Speech recognition failed: {str(e)}'}, status=500)

        post.content = text
        post.save()
        return Response({'text': text, 'message': 'Audio converted to text and saved to post'})

# ----------------------
# Feed API
# ----------------------
class FeedView(generics.ListAPIView):
    """
    Public feed endpoint.
    Automatically translates posts to user's preferred language if ?lang=xx is provided.
    """
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        target_lang = request.query_params.get('lang')  # e.g., ?lang=es
        serialized = self.get_serializer(queryset, many=True).data

        if target_lang:
            for post in serialized:
                if post['content']:
                    post['content_translated'] = GoogleTranslator(
                        source='auto',
                        target=target_lang
                    ).translate(post['content'])

        return Response(serialized)