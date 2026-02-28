from rest_framework import serializers
from .models import User, Post, Follow


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'bio',
            'profile_picture',
            'preferred_language'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'voice_file',
            'media_url',
            'original_language',
            'timestamp'
        ]

    def validate(self, data):
        if not data.get('content') and not data.get('voice_file'):
            raise serializers.ValidationError("Post must contain text or voice.")
        return data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']