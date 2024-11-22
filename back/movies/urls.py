from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 사용자 달력 데이터 조회
    path('calendar/<str:username>/', views.calendar_data_view, name='calendar_data'),
    
    # 추천 영화 생성
    path('recommendations/', views.recommendation_view, name='recommendations'),
    
    # 사용자가 영화를 선택하여 달력에 추가
    path('calendar/<str:username>/select/', views.select_movie, name='select_movie'),
]