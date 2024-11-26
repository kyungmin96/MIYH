from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404, redirect
from .serializers import UserProfileSerializer
from django.conf import settings
from django.shortcuts import redirect
import requests

def kakao_login(request):
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={settings.KAKAO_REST_API_KEY}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
        f"&response_type=code"
    )
    return redirect(kakao_auth_url)

User = get_user_model()

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect

User = get_user_model()

def kakao_callback(request):
    code = request.GET.get('code')
    token_url = "https://kauth.kakao.com/oauth/token"
    profile_url = "https://kapi.kakao.com/v2/user/me"

    # 액세스 토큰 요청
    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": code,
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # if not access_token:
    #     return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 정보 요청
    profile_headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get(profile_url, headers=profile_headers)
    profile_json = profile_response.json()

    kakao_account = profile_json.get("kakao_account", {})
    email = kakao_account.get("email")
    
    # 닉네임 가져오기 (기본값 설정)
    nickname = kakao_account.get("profile", {}).get("nickname", f"user_{profile_json['id']}")

    # if not email:
    #     return Response({"error": "카카오 계정에 이메일이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 생성 또는 로그인 처리
    user, created = User.objects.get_or_create(
        email=email,
        defaults={"username": nickname, "name": nickname}  # name 필드 추가
    )

    # Django 로그인 처리 (세션 기반)
    login(request, user)

    # JSON 응답 반환 (프론트엔드에서 처리)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name  # name 필드 포함
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    serializer = UserProfileSerializer(person, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    User = get_user_model()
    you = get_object_or_404(User, username=username)  # name을 username으로 수정
    me = request.user
    
    if you != me:
        if you.followers.filter(username=me.username).exists():  # name을 username으로 수정
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        
        return Response({
            'is_followed': is_followed,
            'followers_count': you.followers.count(),
            'followings_count': you.followings.count(),
        })
    return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, 
                   status=status.HTTP_400_BAD_REQUEST)