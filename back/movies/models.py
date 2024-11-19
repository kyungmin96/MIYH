# movies/models.py
from django.db import models
from django.conf import settings
from django.db import models

class Genre(models.Model):
    """영화 장르 모델"""
    name = models.CharField(max_length=50)
    tmdb_genre_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    """영화 정보 모델"""
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    tmdb_id = models.IntegerField(unique=True)
    adult = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class DailyMovie(models.Model):
    """일일 추천 영화 모델"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    is_selected = models.BooleanField(default=False)
    recommendation_type = models.CharField(
        max_length=20,
        choices=[
            ('WEATHER', '날씨/기념일 추천'),
            ('POPULAR', '인기 추천')
        ]
    )

    class Meta:
        unique_together = ['user', 'date', 'recommendation_type']

    def __str__(self):
        return f"{self.user.username}'s {self.recommendation_type} movie on {self.date}"