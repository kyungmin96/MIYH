from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    serializer = UserProfileSerializer(person, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    followers = person.followers.all()
    
    # 각 팔로워의 상세 정보를 포함한 리스트 생성
    followers_data = []
    for follower in followers:
        followers_data.append({
            'id': follower.id,
            'username': follower.username,
            'followers_count': follower.followers.count(),
            'is_followed': request.user in follower.followers.all()
        })
    
    return Response(followers_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    you = get_object_or_404(User, pk=user_pk)
    me = request.user
    
    if you != me:
        if you.followers.filter(pk=me.pk).exists():
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