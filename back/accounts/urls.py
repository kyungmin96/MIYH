from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # 커스텀 기능 URLs만 포함
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]