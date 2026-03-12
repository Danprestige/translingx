from django.urls import path
from .views import LikePostView, CommentPostView

app_name = "interactions"

urlpatterns = [

    path("like/<int:post_id>/", LikePostView.as_view(), name="like-post"),

    path("comment/<int:post_id>/", CommentPostView.as_view(), name="comment-post"),

]