# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path('calendar/events/', views.calendar_events, name='calendar-events'),
     path('<int:movie_id>/select/', views.select_movie, name='select-movie'),
     path('fetch/', views.fetch_movies, name='fetch-movies'),
     path('list/', views.movie_list, name='movie-list'),
]