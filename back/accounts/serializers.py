from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer

class CustomLoginSerializer(LoginSerializer):
    email = None 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'password_confirm', 'email')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'password_confirm': {'required': True},
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
        if not data.get('username'):
            raise serializers.ValidationError(
                {"username": "Username field is required."}
            )
        if not data.get('password'):
            raise serializers.ValidationError(
                {"password": "Password field is required."}
            )
        if not data.get('password_confirm'):
            raise serializers.ValidationError(
                {"password_confirm": "Password confirmation is required."}
            )
        if not data.get('email'):
            raise serializers.ValidationError(
                {"email": "Email field is required."}
            )
            
        # 비밀번호 일치 검증
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return data

    def create(self, validated_data):
        # password_confirm 필드 제거
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user