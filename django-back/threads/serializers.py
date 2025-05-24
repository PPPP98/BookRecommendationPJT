from rest_framework import serializers
from .models import Thread, Comment
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_image", "nickname", "bio"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "user"]
        read_only_fields = ["user"]


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ["id", "title", "content", "rating"]


class ThreadDetailSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "content",
            "rating",
            "created_at",
            "updated_at",
            "user",
            "comments",
        ]
