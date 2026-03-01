from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, PostViewSet, FeedView

# ----------------------
# Register viewsets with DRF router
# ----------------------
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)  # fixed typo: 'regisster' → 'register'

# ----------------------
# API URL patterns
# ----------------------
urlpatterns = [
    path('', include(router.urls)),  # /api/users/, /api/posts/
    path('feed/', FeedView.as_view(), name='feed'),  # /api/feed/
    
    # JWT auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # /api/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # /api/token/refresh/
]