# movies/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from .models import Movie, DailyMovie
from .serializers import MovieSerializer, DailyMovieSerializer
import requests

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def calendar_events(request):
    """
    사용자의 캘린더 이벤트(선택한 영화들)를 반환
    """
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    
    # 날짜 범위에 해당하는 선택된 영화들 조회
    events = DailyMovie.objects.filter(
        user=request.user,
        is_selected=True,
        date__range=[start, end] if start and end else [None, None]
    ).select_related('movie')
    
    # FullCalendar 형식으로 데이터 변환
    calendar_events = []
    for event in events:
        calendar_events.append({
            'id': event.id,
            'title': event.movie.title,
            'start': event.date.isoformat(),
            'movie': {
                'id': event.movie.id,
                'title': event.movie.title,
                'poster_path': event.movie.poster_path,
                'overview': event.movie.overview
            }
        })
    
    return Response(calendar_events)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_movie(request, movie_id):
    """
    오늘의 추천 영화 중 하나를 선택
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        today = timezone.now().date()
        
        # 이미 선택된 영화가 있는지 확인
        existing_selection = DailyMovie.objects.filter(
            user=request.user,
            date=today,
            is_selected=True
        ).first()
        
        if existing_selection:
            return Response(
                {"error": "이미 오늘의 영화를 선택하셨습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 새로운 선택 생성
        daily_movie = DailyMovie.objects.create(
            user=request.user,
            movie=movie,
            date=today,
            is_selected=True
        )
        
        serializer = DailyMovieSerializer(daily_movie)
        return Response(serializer.data)
        
    except Movie.DoesNotExist:
        return Response(
            {"error": "영화를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['POST'])
# @permission_classes([IsAdminUser])  # 관리자만 접근 가능
def fetch_movies(request):
    """TMDB API에서 영화 데이터를 가져와 DB에 저장하는 뷰"""
    try:
        from .models import Movie, Genre
        
        # TMDB API 설정
        TMDB_API_KEY = settings.TMDB_API_KEY
        TMDB_BASE_URL = 'https://api.themoviedb.org/3'
        
        # 장르 정보 먼저 가져오기
        genre_response = requests.get(
            f'{TMDB_BASE_URL}/genre/movie/list',
            params={
                'api_key': TMDB_API_KEY,
                'language': 'ko-KR'
            }
        )
        genres_data = genre_response.json()['genres']
        
        # 장르 데이터 저장
        for genre in genres_data:
            Genre.objects.get_or_create(
                tmdb_genre_id=genre['id'],
                defaults={'name': genre['name']}
            )
        
        movies_added = 0
        page = 1
        
        while movies_added < 200:  # 200개의 영화를 저장할 때까지 반복
            # 인기 영화 목록 가져오기
            response = requests.get(
                f'{TMDB_BASE_URL}/movie/popular',
                params={
                    'api_key': TMDB_API_KEY,
                    'language': 'ko-KR',
                    'page': page
                }
            )
            
            if response.status_code != 200:
                return Response(
                    {"error": "TMDB API 요청 실패"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            movies_data = response.json()['results']
            
            for movie_data in movies_data:
                # 성인 영화 제외
                if movie_data['adult']:
                    continue
                
                # 한글 제목이나 설명이 없는 영화 제외
                if not movie_data.get('title') or not movie_data.get('overview'):
                    continue
                
                # 영화 상세 정보 가져오기
                detail_response = requests.get(
                    f'{TMDB_BASE_URL}/movie/{movie_data["id"]}',
                    params={
                        'api_key': TMDB_API_KEY,
                        'language': 'ko-KR'
                    }
                )
                
                if detail_response.status_code == 200:
                    movie_detail = detail_response.json()
                    
                    # 영화 데이터 저장
                    movie, created = Movie.objects.get_or_create(
                        tmdb_id=movie_data['id'],
                        defaults={
                            'title': movie_data['title'],
                            'original_title': movie_data['original_title'],
                            'overview': movie_data['overview'],
                            'release_date': datetime.strptime(
                                movie_data['release_date'], 
                                '%Y-%m-%d'
                            ).date(),
                            'poster_path': movie_data['poster_path'],
                            'backdrop_path': movie_data.get('backdrop_path'),
                            'popularity': movie_data['popularity'],
                            'vote_average': movie_data['vote_average'],
                            'vote_count': movie_data['vote_count'],
                            'adult': movie_data['adult']
                        }
                    )
                    
                    if created:
                        # 장르 연결
                        genres = Genre.objects.filter(
                            tmdb_genre_id__in=movie_data['genre_ids']
                        )
                        movie.genres.set(genres)
                        movies_added += 1
                        
                        if movies_added >= 200:
                            break
            
            page += 1
            if page > 20:  # 최대 20페이지까지만 조회
                break
        
        return Response({
            "message": f"Successfully added {movies_added} movies to database",
            "total_pages_processed": page
        })
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def movie_list(request):
    """저장된 영화 목록을 반환하는 뷰"""
    from .models import Movie
    from .serializers import MovieSerializer
    
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)