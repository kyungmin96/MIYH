# 2024.11.18
일단 백/프론트로 나눠서 해보기. 아이디어 보다 기능적 완성도 일단 만들어 놓기. 시작 페이지 디자인 어떻게 할지 고민. 개인 달력 페이지 만들어 놓는 것 목표

개인달력페이지 만들려다가 로그인, 회원가입, 게시판 페이지 만들기로 선회. 개인달력페이지가 오히려 마지막에 만들어야 했다... 너무 이리저리 데이터 받는거도 많고 복잡해.  pjt8의 코드 긁어다가 postman에 넣고 대강 검증은 했다. dj-resr-auth 인증 기능 넣는 중. 인승의 프론트 코드와 내일 합쳐서 돌아가나 확인할 예정.

# 2024.11.19
로그인 인증까지 진행하고 백/프론트 맞춰보기. 
로그인 / 회원가입 완료! 추후 시간 나면 sns 연동 등 진행 할 수도

게시판과 마이페이지 틀을 잡았다. 게시판은 리뷰/잡담으로 카테고리가 나뉘고, 좋아요 수와 댓글 수를 볼 수 있음. community 앱에 있다. 여기엔 tmdb api에서 영화 목록을 받아온 전체 영화 목록 페이지도 있다. 
마이페이지에는 팔로워수, 팔로잉버튼, 작성글목록, 팔로워 목록이 있다. 그 유저의 오늘의 영화도 들어가야 되는데 아직 안 함. 팔로워 목록에는 그 팔로워의 팔로워 수도 표시 된다. accounts 앱에 위치한다.

생겼던 문제: accounts의 url을 잡을 때 

urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts 관련 URL 패턴 순서 변경 및 통합
    path('accounts/', include('accounts.urls')),  # 커스텀 accounts URL을 먼저 포함
    path('accounts/', include('dj_rest_auth.urls')),  # dj-rest-auth 기본 URL
    path('accounts/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입 URL
    path('movies/', include('movies.urls')),
    path('community/', include('community.urls')),
]

이런식으로 작성되어서 url이 서로 충돌해 표시가 안되는 일이 발생함.


urlpatterns = [
    path('admin/', admin.site.urls),
    # auth 관련 URL과 커스텀 URL을 분리
    path('api/v1/accounts/', include('accounts.urls')),  # 커스텀 accounts URL (프로필, 팔로우 등)
    path('api/auth/', include('dj_rest_auth.urls')),  # 로그인, 로그아웃 등 기본 인증
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('movies/', include('movies.urls')),
    path('community/', include('community.urls')),
]

이런 식으로 재작성하여 구분을 주었다.

나중에 aquerytool 사이트에서 erd 만들어보기

# 2024.11.20
마이페이지에 유저의 오늘의 영화 들어가야함
영화 추천 알고리즘에 챗지피티 api를 이용해보자는 얘기가 나옴... 만드는거 보다 오히려 편할수도?