from rest_framework import serializers
from .models import Post, Comment, PeerProfile


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_name', 'body', 'created_at')
        read_only_fields = ('id', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'author_name', 'title', 'body', 'created_at', 'comments')
        read_only_fields = ('id', 'created_at', 'comments')


class PeerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PeerProfile
        fields = ('id', 'user', 'username', 'total_skill_score', 'rank')
        read_only_fields = ('id',)



