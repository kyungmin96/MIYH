from rest_framework import serializers
from .models import Movie, MovieCalendar

class MovieCalendarSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    poster_path = serializers.CharField(source='movie.poster_path', read_only=True)

    class Meta:
        model = MovieCalendar
        fields = ('id', 'date', 'movie', 'movie_title', 'poster_path')
        read_only_fields = ('user',)

class MovieRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'overview')