from django.urls import path
from .views import CreatePostView, FeedView

app_name = "posts"

urlpatterns = [

    path("create/", CreatePostView.as_view(), name="create-post"),

    path("feed/", FeedView.as_view(), name="feed"),

]