from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Post, Follow


# -----------------------------
# USER SERIALIZER
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'bio',
            'profile_picture'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', '')
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)

        if validated_data.get('password'):
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


# -----------------------------
# POST SERIALIZER
# -----------------------------
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'media_url',
            'timestamp'
        ]


# -----------------------------
# FOLLOW SERIALIZER
# -----------------------------
class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower',
            'following',
            'created_at'
        ]

    def validate(self, data):
        if data['follower'] == data['following']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return data