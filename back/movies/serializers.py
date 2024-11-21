from rest_framework import serializers
from community.models import Movie  # Movie 모델 import 경로 수정
from .models import MovieCalendar

class MovieCalendarSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    poster_path = serializers.CharField(source='movie.poster_path', read_only=True)

    class Meta:
        model = MovieCalendar
        fields = ('id', 'date', 'movie', 'movie_title', 'poster_path', 'latitude', 'longitude')  # 위치 정보 필드 추가
        read_only_fields = ('user',)

class MovieRecommendationSerializer(serializers.ModelSerializer):
    recommendation_reason = serializers.SerializerMethodField()  # 추천 이유 필드 추가

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'overview', 'recommendation_reason')
