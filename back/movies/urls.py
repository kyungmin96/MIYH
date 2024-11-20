from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('calendar/<str:username>/', views.calendar_view, name='calendar'),
    path('calendar/<str:username>/select/', views.select_movie, name='select_movie'),
]