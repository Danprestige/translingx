# core/views.py
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, PostSerializer
from .models import Post

User = get_user_model()


# ----------------------
# User Registration
# ----------------------
class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Anyone can register


# ----------------------
# Post ViewSet
# ----------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    # Example extra action: translate a post
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def translate(self, request, pk=None):
        post = self.get_object()
        # Placeholder translation logic
        translated_content = f"Translated: {post.content}"
        return Response({"id": post.id, "translated_content": translated_content})

    # Example extra action: speech to text
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def speech_to_text(self, request, pk=None):
        post = self.get_object()
        # Placeholder speech-to-text logic
        speech_text = f"Speech-to-text of post {post.id}"
        return Response({"id": post.id, "speech_text": speech_text})


# ----------------------
# Public Feed View
# ----------------------
class FeedAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Public feed accessible without token