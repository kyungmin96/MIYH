from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=20 ,unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    followings = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers'
    )
    
    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username