# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# ----------------------
# Simple root view
# ----------------------
def home(request):
    return HttpResponse("Welcome to TransLingx API 🚀")

# ----------------------
# URL patterns
# ----------------------
urlpatterns = [
    path('', home, name='home'),  # Root
    path('admin/', admin.site.urls),  # Admin panel

    # ----------------------
    # JWT Authentication endpoints
    # ----------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ----------------------
    # Core app API (users, posts, feed, voice uploads)
    # ----------------------
    path('api/', include('core.urls')),  # Include all routes from core app
]

# ----------------------
# Serve media files (for voice uploads) in development
# ----------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)