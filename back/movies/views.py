from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Movie, MovieCalendar
from .serializers import MovieCalendarSerializer, MovieRecommendationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_view(request, username):
    # 요청한 사용자와 달력 주인이 같은지 확인
    if request.user.username != username:
        return Response({'error': '자신의 달력만 볼 수 있습니다.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # 현재 사용자의 캘린더 정보 가져오기
    calendar_entries = MovieCalendar.objects.filter(user=request.user)
    serializer = MovieCalendarSerializer(calendar_entries, many=True)
    
    # 오늘 날짜에 선택한 영화가 있는지 확인
    today = datetime.now().date()
    today_choice = MovieCalendar.objects.filter(
        user=request.user, 
        date=today
    ).first()
    
    if today_choice:
        return Response({
            'has_chosen_today': True,
            'calendar_data': serializer.data
        })
    else:
        recommended_movies = Movie.objects.all().order_by('?')[:2]
        movie_serializer = MovieRecommendationSerializer(recommended_movies, many=True)
        
        return Response({
            'has_chosen_today': False,
            'recommendations': movie_serializer.data,
            'calendar_data': serializer.data
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_movie(request, username):
    # 요청한 사용자와 달력 주인이 같은지 확인
    if request.user.username != username:
        return Response({'error': '자신의 달력에만 영화를 선택할 수 있습니다.'}, 
                       status=status.HTTP_403_FORBIDDEN)

    movie_id = request.data.get('movie_id')
    if not movie_id:
        return Response({'error': '영화를 선택해주세요.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    today = datetime.now().date()
    movie = get_object_or_404(Movie, id=movie_id)
    
    # 이미 오늘 선택한 영화가 있는지 확인
    if MovieCalendar.objects.filter(user=request.user, date=today).exists():
        return Response({'error': '오늘은 이미 영화를 선택하셨습니다.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # 새로운 선택 저장
    calendar_entry = MovieCalendar.objects.create(
        user=request.user,
        movie=movie,
        date=today
    )
    
    serializer = MovieCalendarSerializer(calendar_entry)
    return Response(serializer.data, status=status.HTTP_201_CREATED)