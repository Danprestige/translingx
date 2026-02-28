from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import User, Post, Follow
from .serializers import UserSerializer, PostSerializer, FollowSerializer


# 👤 User CRUD
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# 📝 Post CRUD + Voice Streaming
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    # 🎤 Voice Stream Endpoint
    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        post = self.get_object()
        if post.voice_file:
            return FileResponse(post.voice_file.open(), content_type='audio/mpeg')
        return Response({"error": "No voice file found."})


# 👥 Follow CRUD
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data['follower'] == serializer.validated_data['following']:
            raise serializers.ValidationError("You cannot follow yourself.")
        serializer.save()