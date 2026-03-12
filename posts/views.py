# posts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users

    # GET for testing purposes
    def get(self, request):
        return Response({"message": "Send a POST request to create a post"}, status=200)

    def post(self, request):
        text = request.data.get("text", "")
        voice = request.data.get("voice", None)

        if not text and not voice:
            return Response({"error": "Post must have text or voice"}, status=400)

        post = Post.objects.create(
            user=request.user,  # authenticated user
            text=text,
            voice=voice
        )

        return Response({
            "message": "Post created",
            "post_id": post.id
        }, status=200)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        data = []
        for post in posts:
            data.append({
                "id": post.id,
                "user": post.user.username,
                "text": post.text,
                "voice": str(post.voice) if post.voice else None,
                "created_at": post.created_at
            })
        return Response(data, status=200)