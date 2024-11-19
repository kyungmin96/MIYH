from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 게시글 관련 URL
    path('posts/', views.post_list),
    path('posts/create/', views.post_create),
    path('posts/<int:post_pk>/', views.post_detail_update_delete),
    path('posts/<int:post_pk>/comments/', views.comment_create),
    path('posts/<int:post_pk>/like/', views.post_like),
    
    # 영화 관련 URL
    path('movies/', views.movie_list),
    path('movies/search/', views.movie_search),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/comments/', views.movie_comment_create),
]