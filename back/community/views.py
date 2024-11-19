from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
import requests
from .models import Post, Comment, Movie, MovieComment 
from .serializers import PostSerializer, CommentSerializer, MovieSerializer
from .serializers import (
    PostSerializer, CommentSerializer, 
    MovieSerializer, MovieCommentSerializer
)
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY

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

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    # DB에 저장된 영화가 없거나 업데이트가 필요한 경우 TMDB에서 가져오기
    try:
        movies_data = fetch_popular_movies()
        for movie_data in movies_data.get('results', []):
            # overview나 title이 없는 경우 건너뛰기 (번역되지 않은 영화)
            if not movie_data.get('overview') or not movie_data.get('title'):
                continue
                
            Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'original_title': movie_data['original_title'],
                    'poster_path': movie_data.get('poster_path'),
                    'overview': movie_data.get('overview'),
                    'release_date': movie_data.get('release_date'),
                    'popularity': movie_data.get('popularity', 0)
                }
            )
    except Exception as e:
        print(f"Error fetching movies: {e}")

    # DB에서 인기도순으로 영화 가져오기
    movies = Movie.objects.all().order_by('-popularity')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_search(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({'error': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-KR',
        'query': query,
        'include_adult': False,
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        for movie_data in data.get('results', []):
            if movie_data.get('title') and movie_data.get('overview'):
                Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data['title'],
                        'original_title': movie_data['original_title'],
                        'poster_path': movie_data.get('poster_path'),
                        'overview': movie_data.get('overview'),
                        'release_date': movie_data.get('release_date'),
                        'popularity': movie_data.get('popularity', 0)
                    }
                )
        
        movies = Movie.objects.filter(
            tmdb_id__in=[m['id'] for m in data.get('results', [])]
        )
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)