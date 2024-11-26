from rest_framework import serializers
from .models import MovieCalendar, DayDiary
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
    """달력 데이터를 직렬화"""
    comment = serializers.SerializerMethodField()

    class Meta:
        model = MovieCalendar
        fields = ('id', 'movie_id', 'user', 'tmdb_id', 'title', 'poster_path', 'date', 'comment')
        read_only_fields = ('user',)

    def get_comment(self, obj):
        """해당 날짜의 오늘의 일기를 반환"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            diary = DayDiary.objects.filter(user=request.user, date=obj.date).first()
            return diary.comment if diary else None
        return None

class DayDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayDiary
        fields = ('id', 'user', 'date', 'comment', 'created_at', 'updated_at')