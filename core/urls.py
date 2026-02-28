from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, PostViewSet, FeedView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
]