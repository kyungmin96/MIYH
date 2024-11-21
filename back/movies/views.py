from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.core.cache import cache
from community.models import Movie
from .models import MovieCalendar
from .serializers import MovieCalendarSerializer, MovieRecommendationSerializer
from .utils import get_weather_by_location, check_korean_holiday, get_movie_recommendation, get_time_of_day

def fetch_calendar_data(user, year, month):
    """특정 월의 캘린더 데이터만 조회"""
    return MovieCalendar.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    ).select_related('movie')\
     .only('date', 'movie__id', 'movie__title', 'movie__poster_path')

def check_current_choice(calendar_entries, today):
    """오늘의 선택 영화 확인"""
    return next((entry for entry in calendar_entries if entry.date == today), None)

def get_weather_data(latitude, longitude):
    """날씨 정보 조회"""
    weather_data = get_weather_by_location(latitude, longitude)
    return weather_data['weather'][0]['main'], weather_data['main']['temp']

def determine_season(month):
    """현재 계절 확인"""
    if month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    elif month in [9, 10, 11]:
        return '가을'
    return '겨울'

def get_previous_movie_ids(calendar_entries):
    """이전에 선택한 영화 ID 목록"""
    return {entry.movie_id for entry in calendar_entries}

def fetch_recommended_movies(weather, season, time_of_day, previous_movie_ids, holiday):
    """컨텍스트 기반 영화 추천"""
    cache_key = f'recommended_movie_{weather}_{season}_{time_of_day}_{holiday}'
    cached_movie = cache.get(cache_key)
    if cached_movie:
        return cached_movie

    recommended_tmdb_id, recommendation_type = get_movie_recommendation(
        weather, season, time_of_day, previous_movie_ids, holiday
    )

    if recommended_tmdb_id:
        movie = Movie.objects.filter(tmdb_id=recommended_tmdb_id).first()
        if movie:
            cache.set(cache_key, (movie, recommendation_type), 60 * 30)  # 30분 캐시
            return movie, recommendation_type

    # 추천 실패시 랜덤 선택
    movie = Movie.objects.exclude(id__in=previous_movie_ids).order_by('?').first()
    return movie, 'random'

def fetch_popular_movie(previous_movie_ids, exclude_id=None):
    """인기 영화 추천"""
    cache_key = 'popular_movie'
    cached_movie = cache.get(cache_key)
    if cached_movie and cached_movie.id not in previous_movie_ids:
        return cached_movie

    movies_qs = Movie.objects.exclude(id__in=previous_movie_ids)
    if exclude_id:
        movies_qs = movies_qs.exclude(id=exclude_id)
    
    movie = movies_qs.order_by('-popularity').first()
    if movie:
        cache.set(cache_key, movie, 60 * 15)  # 15분 캐시
    return movie

def fetch_calendar_data(user, year, month):
    """특정 월의 캘린더 데이터만 조회"""
    return MovieCalendar.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    ).select_related('movie')\
     .only('date', 'movie__id', 'movie__title', 'movie__poster_path')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_view(request, username):
    if request.user.username != username:
        return Response({'error': '자신의 달력만 볼 수 있습니다.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # URL 파라미터에서 년도와 월 정보 가져오기
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if not year or not month:
        return Response({'error': '년도와 월 정보가 필요합니다.'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    today = datetime.now().date()
    calendar_entries = fetch_calendar_data(request.user, year, month)
    today_choice = next((entry for entry in calendar_entries 
                        if entry.date == today), None) if int(year) == today.year and int(month) == today.month else None
    
    calendar_serializer = MovieCalendarSerializer(calendar_entries, many=True)
    
    if today_choice:
        return Response({
            'has_chosen_today': True,
            'calendar_data': calendar_serializer.data
        })

    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    if not latitude or not longitude:
        return Response({'error': '위치 정보가 필요합니다.'}, 
                      status=status.HTTP_400_BAD_REQUEST)

    weather, temp = get_weather_data(latitude, longitude)
    season = determine_season(today.month)
    time_of_day = get_time_of_day()
    holiday = check_korean_holiday(today)

    previous_movie_ids = get_previous_movie_ids(calendar_entries)
    context_movie, recommendation_type = fetch_recommended_movies(
        weather, season, time_of_day, previous_movie_ids, holiday
    )
    popular_movie = fetch_popular_movie(
        previous_movie_ids, 
        context_movie.id if context_movie else None
    )

    recommended_movies = [m for m in [context_movie, popular_movie] if m]
    movie_serializer = MovieRecommendationSerializer(recommended_movies, many=True)
    
    return Response({
        'has_chosen_today': False,
        'recommendations': movie_serializer.data,  # 추천된 두 영화
        'calendar_data': calendar_serializer.data  # 달력 데이터
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_movie(request, username):
    if request.user.username != username:
        return Response({'error': '자신의 달력에만 영화를 선택할 수 있습니다.'}, 
                       status=status.HTTP_403_FORBIDDEN)

    movie_id = request.data.get('movie_id')
    if not movie_id:
        return Response({'error': '영화를 선택해주세요.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    today = datetime.now().date()
    movie = get_object_or_404(Movie, id=movie_id)
    
    if MovieCalendar.objects.filter(user=request.user, date=today).exists():
        return Response({'error': '오늘은 이미 영화를 선택하셨습니다.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    calendar_entry = MovieCalendar.objects.create(
        user=request.user,
        movie=movie,
        date=today
    )
    
    serializer = MovieCalendarSerializer(calendar_entry)
    return Response(serializer.data, status=status.HTTP_201_CREATED)