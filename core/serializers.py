# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

# ----------------------
# User Serializer
# ----------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile_picture"]

    def create(self, validated_data):
        """Create user with hashed password"""
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            profile_picture=validated_data.get("profile_picture")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# ----------------------
# Post Serializer
# ----------------------
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    audio_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "author", "content", "audio_file", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        """Assign logged-in user as author"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)