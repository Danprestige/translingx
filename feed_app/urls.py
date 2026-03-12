# feed_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_home, name="feed_home"),
]