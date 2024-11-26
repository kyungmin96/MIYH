from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),  # 카카오 로그인 URL
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),  # 카카오 콜백 URL
]