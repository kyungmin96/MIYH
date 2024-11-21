from rest_framework import serializers
from .models import Post, Comment, Movie, MovieComment  # MovieComment 추가
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class MovieCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MovieComment
        fields = ('id', 'user', 'content', 'movie', 'created_at')
        read_only_fields = ('movie',)

class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    comments = MovieCommentSerializer(many=True, read_only=True)  # 한줄평 추가
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # 한줄평 개수 추가
    
    class Meta:
        model = Movie
        fields = ('id', 'tmdb_id', 'title', 'original_title', 'poster_path', 
                 'overview', 'release_date', 'popularity', 'poster_url',
                 'comments', 'comments_count')  # 필드 추가

    def get_poster_url(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)  # 날짜 포맷 지정

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'post', 'created_at')
        read_only_fields = ('post',)

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # 댓글 개수 추가
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)  # 날짜 포맷 지정
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)  # 날짜 포맷 지정

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category', 'content', 'image',
                  'comments', 'comments_count',
                 'created_at', 'updated_at', 'like_users_count', 'is_liked')
        read_only_fields = ('like_users_count', 'comments_count')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False
        