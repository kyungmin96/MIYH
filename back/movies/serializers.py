# movies/serializers.py
from rest_framework import serializers
from .models import Movie, DailyMovie

class MovieSerializer(serializers.ModelSerializer):
    """영화 정보를 직렬화하는 시리얼라이저"""
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_path', 'overview', 'release_date']

class DailyMovieSerializer(serializers.ModelSerializer):
    """일일 추천 영화 정보를 직렬화하는 시리얼라이저"""
    # 중첩된 영화 정보를 포함
    movie = MovieSerializer()
    
    class Meta:
        model = DailyMovie
        fields = ['id', 'movie', 'date', 'is_selected', 'recommendation_type']

class CalendarEventSerializer(serializers.ModelSerializer):
    """캘린더 이벤트 형식으로 영화 정보를 직렬화하는 시리얼라이저"""
    # FullCalendar에서 요구하는 필드명으로 매핑
    title = serializers.CharField(source='movie.title')  # 이벤트 제목으로 영화 제목 사용
    start = serializers.DateField(source='date')  # 이벤트 시작일로 추천 날짜 사용
    poster_path = serializers.CharField(source='movie.poster_path')  # 영화 포스터 경로

    class Meta:
        model = DailyMovie
        fields = ['id', 'title', 'start', 'poster_path']