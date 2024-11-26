from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth 관련 URL과 커스텀 URL을 분리
    path('api/v1/accounts/', include('accounts.urls')),  # 커스텀 accounts URL (프로필, 팔로우 등)
    path('api/auth/', include('dj_rest_auth.urls')),  # 로그인, 로그아웃 등 기본 인증
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('movies/', include('movies.urls')),
    path('community/', include('community.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)