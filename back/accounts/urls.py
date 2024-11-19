from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # dj-rest-auth 기본 인증 URLs
    path('', include('dj_rest_auth.urls')),
    # 회원가입을 위한 URLs (registration 기능 사용 시)
    path('registration/', include('dj_rest_auth.registration.urls')),
    
    # 커스텀 기능 URLs
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]