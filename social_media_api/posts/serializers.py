from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username',
            'title', 'content',
            'likes_count', 'comments_count', 'comments',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
