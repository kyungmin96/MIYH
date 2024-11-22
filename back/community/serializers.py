from rest_framework import serializers
from .models import Post, Comment, Movie, MovieComment  # MovieCalendar 추가
from django.contrib.auth import get_user_model
from movies.models import MovieCalendar
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class MovieCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # 사용자 정보에 name 포함

    class Meta:
        model = MovieComment
        fields = ('id', 'user', 'content', 'movie', 'created_at')
        read_only_fields = ('movie',)

    def get_user(self, obj):
        """작성자 정보 반환"""
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "name": obj.user.name  # name 필드 추가
        }

class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    comments = MovieCommentSerializer(many=True, read_only=True)  # 한줄평 추가
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # 한줄평 개수 추가
    is_in_calendar = serializers.SerializerMethodField()  # 사용자의 달력 여부 확인

    class Meta:
        model = Movie
        fields = ('id', 'tmdb_id', 'title', 'original_title', 'poster_path', 
                 'overview', 'release_date', 'popularity', 'poster_url',
                 'comments', 'comments_count', 'is_in_calendar')  # 필드 추가

    def get_poster_url(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None

    def get_is_in_calendar(self, obj):
        """사용자가 이 영화를 달력에 추가했는지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return MovieCalendar.objects.filter(user=request.user, tmdb_id=obj.tmdb_id).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # 사용자 정보에 name 포함

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'post', 'created_at')
        read_only_fields = ('post',)

    def get_user(self, obj):
        """작성자 정보 반환"""
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "name": obj.user.name  # name 필드 추가
        }

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
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
    
    def get_user(self, obj):
        """작성자 정보 반환"""
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "name": obj.user.name  # name 필드 추가
        }
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False

class MovieCalendarSerializer(serializers.ModelSerializer):
    """달력 데이터를 직렬화"""
    class Meta:
        model = MovieCalendar
        fields = ('id', 'user', 'tmdb_id', 'title', 'poster_path', 'date')
        read_only_fields = ('user',)
