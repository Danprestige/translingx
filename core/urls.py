# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterAPIView, PostViewSet, FeedAPIView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    # User registration
    path('users/register/', UserRegisterAPIView.as_view(), name='user_register'),

    # Public feed
    path('feeds/', FeedAPIView.as_view(), name='feeds'),

    # Post routes (CRUD + extra actions like translate/speech_to_text)
    path('', include(router.urls)),
]