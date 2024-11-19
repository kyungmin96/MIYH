from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    # 리뷰 목록 조회
    path('reviews/', views.index, name='index'),
    
    # 리뷰 생성
    path('reviews/create/', views.create, name='create'),
    
    # 리뷰 상세 조회
    path('reviews/<int:review_pk>/', views.detail, name='detail'),
    
    # 댓글 생성
    path(
        'reviews/<int:review_pk>/comments/',
        views.create_comment,
        name='create_comment',
    ),
    
    # 좋아요 토글
    path('reviews/<int:review_pk>/like/', views.like, name='like'),
]