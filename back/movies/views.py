from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from accounts.models import User
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import MovieCalendar, DayDiary
from .serializers import MovieCalendarSerializer, MovieRecommendationSerializer, DayDiarySerializer
from .utils import get_weather_by_location, check_korean_holiday, get_movie_recommendation, get_time_of_day, get_tmdb_movie
from community.models import Movie
from .utils import get_popular_movies

def fetch_calendar_data(user, year, month):
    """특정 월의 캘린더 데이터만 조회"""
    return MovieCalendar.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

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

def get_previous_tmdb_ids(calendar_entries):
    """이전에 선택한 영화 TMDB ID 목록"""
    return {entry.tmdb_id for entry in calendar_entries}

def fetch_recommended_movies(weather, season, time_of_day, previous_tmdb_ids, holiday, username):
    today = datetime.now().date()
    cache_key = f'movie_recommendation_{username}_{today}_{hash(str(previous_tmdb_ids))}'
    cached_movie = cache.get(cache_key)

    if cached_movie:
        return cached_movie

    recommended_tmdb_id, recommendation_type = get_movie_recommendation(
        weather, season, time_of_day, previous_tmdb_ids, holiday
    )

    if recommended_tmdb_id:
        movie_data = get_tmdb_movie(recommended_tmdb_id)
        if movie_data:
            # 전체 영화 목록에 추가
            Movie.objects.update_or_create(
                tmdb_id=movie_data['tmdb_id'],  # TMDB ID를 기준으로 저장
                defaults={
                    'title': movie_data['title'],
                    'poster_path': movie_data.get('poster_path'),
                    'overview': movie_data.get('overview'),
                    'release_date': movie_data.get('release_date'),
                    'popularity': movie_data.get('popularity', 0),
                }
            )
            result = (movie_data, recommendation_type)
            tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
            cache_timeout = int((tomorrow - datetime.now()).total_seconds())
            cache.set(cache_key, result, timeout=cache_timeout)
            return result

    return None, None

def fetch_popular_movie(previous_tmdb_ids, exclude_tmdb_id=None, username=None):
    today = datetime.now().date()
    cache_key = f'popular_movie_{username}_{today}'
    cached_movie = cache.get(cache_key)

    if cached_movie:
        return cached_movie

    popular_movies = get_popular_movies()

    for movie in popular_movies:
        if movie['id'] not in previous_tmdb_ids and movie['id'] != exclude_tmdb_id:
            movie_data = get_tmdb_movie(movie['id'])
            if movie_data:
                # 전체 영화 목록에 추가
                Movie.objects.update_or_create(
                    tmdb_id=movie_data['tmdb_id'],  # TMDB ID를 기준으로 저장
                    defaults={
                        'title': movie_data['title'],
                        'poster_path': movie_data.get('poster_path'),
                        'overview': movie_data.get('overview'),
                        'release_date': movie_data.get('release_date'),
                        'popularity': movie_data.get('popularity', 0),
                    }
                )
                tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
                cache_timeout = int((tomorrow - datetime.now()).total_seconds())
                cache.set(cache_key, movie_data, timeout=cache_timeout)
                return movie_data

    return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_view(request):
    user = request.user
    username = user.username

    latitude = request.GET.get('latitude', 37.5665)  # 서울의 위도 (기본값)
    longitude = request.GET.get('longitude', 126.9780)  # 서울의 경도 (기본값)

    weather, temp = get_weather_data(latitude, longitude)
    season = determine_season(datetime.now().month)
    time_of_day = get_time_of_day()
    holiday = check_korean_holiday(datetime.now().date())

    previous_tmdb_ids = get_previous_tmdb_ids(MovieCalendar.objects.filter(user=user))

    # 첫 번째 추천 (컨텍스트 기반)
    context_movie, recommendation_type = fetch_recommended_movies(
        weather, season, time_of_day, previous_tmdb_ids, holiday, username
    )

    # 두 번째 추천 (인기 영화)
    popular_movie = fetch_popular_movie(
        previous_tmdb_ids,
        context_movie['tmdb_id'] if context_movie else None,
        username
    )

    # 두 결과가 모두 준비될 때까지 대기
    while not context_movie or not popular_movie:
        if not context_movie:
            context_movie, recommendation_type = fetch_recommended_movies(
                weather, season, time_of_day, previous_tmdb_ids, holiday, username
            )
        if not popular_movie:
            popular_movie = fetch_popular_movie(
                previous_tmdb_ids,
                context_movie['tmdb_id'] if context_movie else None,
                username
            )

    recommended_movies = [m for m in [context_movie, popular_movie] if m]
    
    movie_serializer = MovieRecommendationSerializer(recommended_movies, many=True)

    return Response({
        'recommendations': movie_serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_data_view(request, username):
    """사용자의 개인 달력 데이터를 반환"""
    user = get_object_or_404(User, username=username)
    year = int(request.query_params.get('year', datetime.now().year))
    month = int(request.query_params.get('month', datetime.now().month))

    # 해당 연도 및 월의 달력 데이터를 가져옴
    calendar_entries = MovieCalendar.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )
    
    # 데이터 확인을 위한 로깅
    print("Calendar Entries:", calendar_entries.values())
    
    serializer = MovieCalendarSerializer(calendar_entries, many=True, context={'request': request})
    serialized_data = serializer.data
    
    # 직렬화된 데이터 확인을 위한 로깅
    print("Serialized Data:", serialized_data)
    
    return Response(serialized_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_movie(request, username):
    if request.user.username != username:
        return Response({'error': '자신의 달력에만 영화를 선택할 수 있습니다.'}, 
                        status=status.HTTP_403_FORBIDDEN)

    tmdb_id = request.data.get('tmdb_id')
    if not tmdb_id:
        return Response({'error': '영화를 선택해주세요.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    today = datetime.now().date()

    # TMDB API에서 영화 데이터 가져오기
    movie_data = get_tmdb_movie(tmdb_id)
    if not movie_data:
        return Response({'error': '유효하지 않은 영화입니다.'}, 
                        status=status.HTTP_400_BAD_REQUEST)

    # Movie 객체 가져오기 또는 생성하기
    movie, _ = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            'title': movie_data['title'],
            'poster_path': movie_data['poster_path']
        }
    )

    # 달력 데이터를 업데이트하거나 새로 생성
    calendar_entry, _ = MovieCalendar.objects.update_or_create(
        user=request.user,
        date=today,
        defaults={
            'movie_id': movie.id,  # movie_id를 올바르게 설정
            'tmdb_id': movie_data['tmdb_id'],
            'title': movie_data['title'],
            'poster_path': movie_data['poster_path'],
        }
    )

    serializer = MovieCalendarSerializer(calendar_entry)
    print("Movie ID:", movie.id)
    print("Calendar Entry:", calendar_entry.__dict__)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def day_diary_create_or_update(request):
    """오늘의 일기를 생성하거나 수정"""
    comment_text = request.data.get('comment')
    if not comment_text:
        return Response({'error': '일기 내용을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    today = datetime.now().date()

    # 오늘 날짜에 해당하는 일기를 생성 또는 수정
    diary, created = DayDiary.objects.update_or_create(
        user=request.user,
        date=today,
        defaults={'comment': comment_text}
    )

    if created:
        message = "오늘의 일기가 작성되었습니다."
        status_code = status.HTTP_201_CREATED
    else:
        message = "오늘의 일기가 수정되었습니다."
        status_code = status.HTTP_200_OK

    serializer = DayDiarySerializer(diary)
    return Response({'message': message, 'data': serializer.data}, status=status_code)