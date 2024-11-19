from rest_framework import serializers
from .models import Review, Comment
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'review', 'created_at', 'updated_at')
        read_only_fields = ('review',)

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'user', 'title', 'content', 'comments', 
                 'created_at', 'updated_at', 'like_users_count', 'is_liked')

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.like_users.filter(pk=user.pk).exists()
        return False