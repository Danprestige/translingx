# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return HttpResponse("🚀 Welcome to TransLingx Social app API")


urlpatterns = [

    path("", home),

    path("admin/", admin.site.urls),

    # JWT AUTH
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),

    #streams
    path("api/streams", include("streams.urls")),

    path("api/feed/", include("feed_app.urls")),

    # Interactions
    path("api/interactions/", include("interactions.urls")),

    #posts
    path("api/posts/", include("posts.urls")),
]
    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)