from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import User, Post, Follow
from .serializers import UserSerializer, PostSerializer


# -----------------------------------
# Custom Permission: Owner Only Edit
# -----------------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.user == request.user


# -----------------------------------
# USER VIEWSET
# -----------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()

        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=400)

        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        return Response({"message": "Followed successfully"})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()

        Follow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).delete()

        return Response({"message": "Unfollowed successfully"})


# -----------------------------------
# POST VIEWSET
# -----------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -----------------------------------
# FEED VIEW
# -----------------------------------
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get users the current user follows
        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list('following', flat=True)

        # Get posts from followed users
        posts = Post.objects.filter(
            user__in=following_users
        ).order_by('-timestamp')

        # Optional search filter
        search_query = request.query_params.get('search')
        if search_query:
            posts = posts.filter(
                Q(content__icontains=search_query)
            )

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)