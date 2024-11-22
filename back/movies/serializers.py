from rest_framework import serializers
from .models import MovieCalendar
from community.models import Movie

class MovieRecommendationSerializer(serializers.Serializer):
    movie_id = serializers.SerializerMethodField()  # 전체 영화 목록의 ID
    title = serializers.CharField()  # 영화 제목
    poster_path = serializers.CharField()  # 포스터 경로
    overview = serializers.CharField()  # 영화 줄거리

    def get_movie_id(self, obj):
        """TMDB ID를 기반으로 Movie 모델의 id 반환"""
        movie = Movie.objects.filter(tmdb_id=obj['tmdb_id']).first()
        return movie.id if movie else None
    
class MovieCalendarSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField()  # Movie 모델의 id를 가져오는 커스텀 필드

    class Meta:
        model = MovieCalendar
        fields = ('id', 'date', 'title', 'poster_path', 'movie_id')  # movie_id 추가

    def get_movie_id(self, obj):
        """TMDB ID를 기반으로 Movie 모델의 id 반환"""
        movie = Movie.objects.filter(tmdb_id=obj.tmdb_id).first()
        return movie.id if movie else None