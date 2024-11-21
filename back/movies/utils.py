# utils.py
import requests
from django.core.cache import cache
from datetime import datetime, timedelta
from openai import OpenAI
from django.conf import settings
import random
from community.models import Movie

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return '아침'
    elif 12 <= hour < 17:
        return '오후'
    elif 17 <= hour < 20:
        return '저녁'
    else:
        return '밤'

def get_weather_by_location(lat, lon):
    cache_key = f'weather_{lat}_{lon}'
    cached_weather = cache.get(cache_key)
    
    if cached_weather:
        return cached_weather

    try:
        weather_api_key = settings.OPENWEATHER_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
        response = requests.get(url, timeout=5)
        weather_data = response.json()
        # 날씨 정보를 1시간 동안 캐시
        cache.set(cache_key, weather_data, 60 * 60)
        return weather_data
    except requests.Timeout:
        # 기본 날씨 정보 반환
        return {'weather': [{'main': 'Clear'}], 'main': {'temp': 20}}

def check_korean_holiday(date):
    holidays = {
        '0301': ('삼일절', '독립운동, 역사'),
        '0505': ('어린이날', '가족, 어린이'),
        '0606': ('현충일', '전쟁, 호국'),
        '0815': ('광복절', '독립운동, 역사'),
        '1003': ('개천절', '한국 역사, 건국'),
        '1009': ('한글날', '한국 문화'),
    }
    date_str = date.strftime('%m%d')
    return holidays.get(date_str)

def get_movie_recommendation(weather, season, time_of_day, previous_movies, holiday=None):
    # previous_movies를 tmdb_id 목록으로 변환
    previous_tmdb_ids = Movie.objects.filter(id__in=previous_movies).values_list('tmdb_id', flat=True)
    excluded_movies = ', '.join(map(str, previous_tmdb_ids))
    
    if holiday:
        prompt = f"""오늘은 {holiday[0]}입니다. {holiday[1]} 관련 영화를 추천해주세요.
                    다음 TMDB ID를 가진 영화들은 제외해주세요: {excluded_movies}
                    TMDB ID로만 응답해주세요."""
        recommendation_type = "holiday"
    else:
        recommendation_type = random.choice(['weather', 'time'])
        if recommendation_type == 'weather':
            prompt = f"""날씨가 {weather}이고 {season}인 상황에 어울리는 영화를 추천해주세요.
                        다음 TMDB ID를 가진 영화들은 제외해주세요: {excluded_movies}
                        TMDB ID로만 응답해주세요."""
        else:
            prompt = f"""하루 중 {time_of_day} 시간대에 보기 좋은 영화를 추천해주세요.
                        다음 TMDB ID를 가진 영화들은 제외해주세요: {excluded_movies}
                        TMDB ID로만 응답해주세요."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 영화 추천 전문가입니다. TMDB ID로만 응답해주세요."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        recommended_tmdb_id = int(response.choices[0].message.content.strip())
        return recommended_tmdb_id, recommendation_type
            
    except (ValueError, TypeError):
        # GPT가 tmdb_id가 아닌 다른 형식으로 응답한 경우
        return None, recommendation_type