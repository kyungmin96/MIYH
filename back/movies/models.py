# movies/models.py
from django.db import models
from django.conf import settings
from community.models import Movie  # community 앱의 Movie 모델 import

class MovieCalendar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s choice on {self.date}"