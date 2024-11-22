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

전체 영화페이지에서 감독, 출연 데이터 넘겨주기. 그리고 댓글에 평점 입력 될 수 있도록 공간 만들어주기

community/movie에서 comment , comments 중복 되어 있는거 하나 지우기 

리뷰랑 잡담은 카테고리만 다르고 형식은 같도록 수정 -> serializer.py 수정해서 처리. 불필요한 필드도 줄였음

현재 openweather api에서 정보를 불러올 때 너무 오래 걸린다.  get_weather_by_location 함수 수정 꼭 필요.ORD 구조를 간략화 해달라고 했는데도 잘 안된다.....
이전에 선택한 영화가 추천에 뜨지 않게 하는 로직이 잘못 됐다. 이걸 빼고 갈 수는 없으니 고쳐봐야 겠다...
그걸 수정했는데 여전히 6초대. 내일 계속 고쳐보고...
추천된 두 영화도 지금 안 반환되고 있다. 해결해야함

마이페이지에 팔로잉, 팔로워 목록 다 넣도록 수정.->완료!


# 2024.11.21
마이페이지 수정 완료! url 헷갈려서 바보짓함...
profile 작성 글 목록에서 좋아요 수랑 댓글 수도 넘겨주도록 수정하기

추천 두가지를 할 때 tmdb api를 community 앱의 movies url에서 import를 해 받아오다 보니 그걸 안 실행 시키면 영화 목록을 찾지못해서 깡통이 반환된다. 떼어놔야 하나?

# 2024.11.22
프로필을 username이 아닌 nickname으로 접근하도록 url과 view 수정. id는 로그인할때만 쓰고 웬만한 url 다 nickname으로 쓰도록...

남의 프로필에서 '달력보기' 누르면 그 사람 달력 볼 수 있도록. 지금은 자기 달력만 볼 수 있움 -> 인승이가 프론트에서 처리해주기로 함!

추천 영화들이 movie_serach 거치는지 확인. 아니면 거치도록 -> 굳이 안그래도 추천 과정에서 전체 영화 목록으로 들어가도록 수정했다!

닉네임 수정 고려하기

닉네임 필요한곳
마이페이지 팔로워 팔로잉 리스트
영화 상세 페이지, 게시판 전체 글 및 상세 페이지 -> 모두 추가함!

영화 추천 두 알고리즘이 속도가 달라서 하나만 반환되는 상황 발생. 비동기 처리로 해결해 보려는중... -> 비동기 처리는 에바였고 두개가 다 들어오기까지 기다리는 식으로 변경!

댓글 삭제 기능도 추가!

영화 추천 알고리즘 중 인기 영화는 랜덤으로 골라오게 할려고 했는데 너무 오래 걸리네.. 랜덤도 아님. 다음주에 와서 그냥 랜덤성 없엔 원래 코드로 돌아