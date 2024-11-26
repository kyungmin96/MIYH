from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=200, null=True)
    overview = models.TextField(null=True)
    release_date = models.DateField(null=True)
    popularity = models.FloatField(default=0)
    youtube_url = models.URLField(max_length=500, null=True, blank=True)  # YouTube URL 추가

    def __str__(self):
        return self.title
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    class Meta:
        ordering = ['-popularity']

class MovieComment(models.Model):
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.movie.title} - {self.user.username}'

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('review', '리뷰'),
        ('talk', '잡담'),
    ]
    
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('5.0'))
        ],
        null=True,
        blank=True
    )
    like_users = models.ManyToManyField(  # 좋아요 필드가 빠져있었습니다
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        blank=True
    )

    def __str__(self):
        return self.title

    @property  # property 데코레이터 사용
    def comments_count(self):
        return self.comments.count()
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 추가

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.post.title} - {self.user.username}'