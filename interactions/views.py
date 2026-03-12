# interactions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Like, Comment
from posts.models import Post

User = get_user_model()

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        
        # Prevent duplicate likes by same user
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"error": "You have already liked this post"}, status=400)

        Like.objects.create(post=post, user=request.user)
        return Response({"message": f"Post {post_id} liked"}, status=200)


class CommentPostView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def post(self, request, post_id):
        content = request.data.get("content", "").strip()
        if not content:
            return Response({"error": "Content is required"}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        Comment.objects.create(post=post, user=request.user, content=content)
        return Response({"message": f"Comment added to post {post_id}"}, status=200)