from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from community.models import Post

class CustomRegisterSerializer(RegisterSerializer):
    # RegisterSerializer에는 이미 username, password1, password2, email이 있음
    name = serializers.CharField(required=True, write_only=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data.get('name')
        user.save()
        return user

class CustomLoginSerializer(LoginSerializer):
    # 로그인 시 username과 password만 필요하도록 email 필드 제외
    email = None 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_confirm', 'name', 'email')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'password_confirm': {'required': True},
            'name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # 허용되지 않은 필드 검사
        allowed_fields = set(self.fields.keys())
        received_fields = set(self.initial_data.keys())
        unknown_fields = received_fields - allowed_fields
        
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown field(s): {', '.join(unknown_fields)}. Only {', '.join(allowed_fields)} are allowed."
            )

        # 필수 필드 검증
        required_fields = ['username', 'password', 'password_confirm', 'name', 'email']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    {field: f"{field.capitalize()} field is required."}
                )
            
        # 비밀번호 일치 검증
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError(
                {"password_confirm": "비밀번호가 일치하지 않습니다."}
            )

        return data

    def create(self, validated_data):
        # password_confirm 필드 제거
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            pal=validated_data['pal'],
            email=validated_data['email']
        )
        return user

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content')

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    followers_list = serializers.SerializerMethodField()
    followings_list = serializers.SerializerMethodField()  # 팔로잉 목록 추가
    posts = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'followers_count', 'followings_count', 
                 'followers_list', 'followings_list', 'posts', 'is_me', 'is_followed')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_list(self, obj):
        return [{
            'id': follower.id,
            'username': follower.username,
            'followers_count': follower.followers.count(),
            'is_followed': self.context.get('request').user in follower.followers.all() if self.context.get('request') else False
        } for follower in obj.followers.all()]

    def get_followings_list(self, obj):
        return [{
            'id': following.id,
            'username': following.username,
            'followers_count': following.followers.count(),
            'is_followed': self.context.get('request').user in following.followers.all() if self.context.get('request') else False
        } for following in obj.followings.all()]

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj).order_by('-created_at')
        return [{
            'id': post.id,
            'title': post.title,
            'content_preview': post.content[:100]  # 내용 미리보기 100자
        } for post in posts]

    def get_is_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj == request.user
        return False

    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(pk=request.user.pk).exists()
        return False