from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from datetime import datetime
import requests
from .models import Post, Movie, Comment, MovieComment
from .serializers import PostSerializer, CommentSerializer, MovieSerializer
from .serializers import (
    PostSerializer, CommentSerializer, 
    MovieSerializer, MovieCommentSerializer
)
from movies.models import MovieCalendar
from movies.serializers import MovieCalendarSerializer
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY

def fetch_youtube_url(tmdb_id):
    """
    TMDB API를 통해 특정 영화의 YouTube 예고편 URL 가져오기
    """
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos"
    params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            videos = response.json().get('results', [])
            for video in videos:
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except requests.RequestException as e:
        print(f"Error fetching YouTube URL: {e}")
        return None

def fetch_popular_movies():
    url = f'https://api.themoviedb.org/3/discover/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-KR',
        'sort_by': 'popularity.desc',
        'include_adult': False,
        'page': 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        movies_data = response.json().get('results', [])
        for movie_data in movies_data:
            # overview나 title이 없는 경우 건너뛰기
            if not movie_data.get('overview') or not movie_data.get('title'):
                continue
            
            # DB에 저장 또는 업데이트 (id를 tmdb_id로 매핑)
            Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],  # 여기서 id를 tmdb_id로 저장
                defaults={
                    'title': movie_data['title'],
                    'original_title': movie_data['original_title'],
                    'poster_path': movie_data.get('poster_path'),
                    'overview': movie_data.get('overview'),
                    'release_date': movie_data.get('release_date'),
                    'popularity': movie_data.get('popularity', 0),
                }
            )
    return response.json()


@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    category = request.query_params.get('category', None)
    if category:
        posts = Post.objects.filter(category=category).order_by('-pk')
    else:
        posts = Post.objects.order_by('-pk')
        
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = PostSerializer(post, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 작성자 본인만 삭제 가능
    if comment.user != request.user:
        return Response({'error': '댓글을 삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    return Response({
        'is_liked': is_liked,
        'likes_count': post.like_users.count()
    })

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail_update_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 작성자 본인만 수정/삭제 가능
    if request.method in ['PUT', 'DELETE'] and post.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def fetch_tmdb_api(endpoint, params):
    base_url = "https://api.themoviedb.org/3"
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"TMDB API Error: {e}")
        return None


def is_adult_movie(movie_id):
    """Check if a movie is adult based on certification."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
    params = {"api_key": TMDB_API_KEY}
    
    try:
        data = fetch_tmdb_api(f"movie/{movie_id}/release_dates", params)
        if not data:
            return False
        
        for result in data.get("results", []):
            # Check for Korean (KR) certification
            if result['iso_3166_1'] == 'KR':
                for release in result['release_dates']:
                    if release['certification'] == '청소년관람불가':
                        return True
            
            # Check for US certification (R or NC-17)
            if result['iso_3166_1'] == 'US':
                for release in result['release_dates']:
                    if release['certification'] in ['R', 'NC-17']:
                        return True
        return False
    except Exception as e:
        print(f"Error checking certification: {e}")
        return False


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_calendar(request):
    """사용자의 달력에 영화를 추가하거나 업데이트"""
    tmdb_id = request.data.get('tmdb_id')
    title = request.data.get('title')
    poster_path = request.data.get('poster_path')

    # 필수 데이터 확인
    if not tmdb_id or not title or not poster_path:
        return Response({'error': '필수 데이터가 누락되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    today = datetime.now().date()

    # 오늘 날짜의 달력 데이터를 가져옴 (존재하면 업데이트, 없으면 생성)
    calendar_entry, created = MovieCalendar.objects.update_or_create(
        user=request.user,
        date=today,
        defaults={
            'tmdb_id': tmdb_id,
            'title': title,
            'poster_path': poster_path,
        }
    )

    # 응답 메시지 설정
    if created:
        message = "영화가 달력에 추가되었습니다."
        status_code = status.HTTP_201_CREATED
    else:
        message = "추천 영화가 업데이트되었습니다."
        status_code = status.HTTP_200_OK

    serializer = MovieCalendarSerializer(calendar_entry)
    return Response({'message': message, 'data': serializer.data}, status=status_code)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    """전체 영화 목록을 반환"""
    try:
        movies_data = fetch_popular_movies()  # 여기서 사용
        for movie_data in movies_data.get('results', []):
            # overview나 title이 없는 경우 건너뛰기
            if not movie_data.get('overview') or not movie_data.get('title'):
                continue

            youtube_url = fetch_youtube_url(movie_data['id'])  # YouTube URL 가져오기

            # DB 업데이트 또는 생성
            Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'original_title': movie_data['original_title'],
                    'poster_path': movie_data.get('poster_path'),
                    'overview': movie_data.get('overview'),
                    'release_date': movie_data.get('release_date'),
                    'popularity': movie_data.get('popularity', 0),
                    'youtube_url': youtube_url,  # YouTube URL 저장
                }
            )
        
        # DB에서 인기도순으로 영화 가져오기
        movies = Movie.objects.all().order_by('-popularity')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_recommendation(request, movie_pk):
    """추천받은 영화를 달력에 추가"""
    # movie_pk를 사용하여 영화 데이터를 가져옴
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # 필요한 데이터 추출
    tmdb_id = movie.tmdb_id
    title = movie.title
    poster_path = movie.poster_path

    # 오늘 날짜 확인
    today = datetime.now().date()

    # 달력에 이미 추가된 경우 업데이트, 없으면 생성
    calendar_entry, created = MovieCalendar.objects.update_or_create(
        user=request.user,
        date=today,
        defaults={
            'tmdb_id': tmdb_id,
            'title': title,
            'poster_path': poster_path,
        }
    )

    # 응답 메시지 설정
    if created:
        message = "영화가 달력에 추가되었습니다."
        status_code = status.HTTP_201_CREATED
    else:
        message = "추천 영화가 업데이트되었습니다."
        status_code = status.HTTP_200_OK

    serializer = MovieCalendarSerializer(calendar_entry)
    return Response({'message': message, 'data': serializer.data}, status=status_code)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieCommentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def movie_comment_delete(request, comment_pk):
    comment = get_object_or_404(MovieComment, pk=comment_pk)

    # 작성자 본인만 삭제 가능
    if comment.user != request.user:
        return Response({'error': '댓글을 삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_search(request):
    """검색어를 기반으로 영화를 검색"""
    query = request.query_params.get('query', '')
    
    if not query:
        return Response({'error': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ko-KR",
        "query": query,
        "include_adult": False,
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        valid_movies = []
        
        for movie_data in data.get('results', []):
            # overview와 title이 없는 영화 건너뛰기
            if not movie_data.get('title') or not movie_data.get('overview'):
                continue
            
            # 성인물 필터링
            if is_adult_movie(movie_data['id']):
                continue
            
            youtube_url = fetch_youtube_url(movie_data['id'])  # YouTube URL 가져오기
            valid_movies.append(movie_data)
            
            # DB 업데이트 또는 생성
            Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'original_title': movie_data['original_title'],
                    'poster_path': movie_data.get('poster_path'),
                    'overview': movie_data.get('overview'),
                    'release_date': movie_data.get('release_date'),
                    'popularity': movie_data.get('popularity', 0),
                    'youtube_url': youtube_url,  # YouTube URL 저장
                }
            )
        
        serializer = MovieSerializer(valid_movies, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        print(f"Error searching movies: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)