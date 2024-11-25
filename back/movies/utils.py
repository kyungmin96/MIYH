import requests
from django.core.cache import cache
from datetime import datetime, timedelta
from openai import OpenAI
from django.conf import settings
import random

client = OpenAI(api_key=settings.OPENAI_API_KEY)
tmdb_api_key = settings.TMDB_API_KEY

def is_adult_movie(movie_id):
    """
    Check if a movie is adult based on certification.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
    params = {"api_key": tmdb_api_key}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for result in data.get("results", []):
                # Check for Korean (KR) certification
                if result['iso_3166_1'] == 'KR':
                    for release in result['release_dates']:
                        if release['certification'] == '청소년관람불가':
                            return True
                # Check for US certification (R or NC-17)
                if result['iso_3166_1'] == 'US':
                    for release in result['release_dates']:
                        if release['certification'] in ['R', 'NC-17']:
                            return True
        return False
    except Exception as e:
        print(f"Error checking certification: {e}")
        return False

def fetch_youtube_url(tmdb_id):
    """TMDB API를 통해 특정 영화의 YouTube 예고편 URL 가져오기"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos"
    params = {"api_key": tmdb_api_key, "language": "ko-KR"}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            videos = response.json().get('results', [])
            for video in videos:
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except requests.RequestException as e:
        print(f"Error fetching YouTube URL: {e}")
        return None

def get_tmdb_movie(tmdb_id):
    """TMDB API를 통해 영화 정보 가져오기"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}&language=ko-KR"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # 성인물 제외
            if data.get('adult', False):
                return None
            # 한국어 정보가 없는 경우 제외
            if not data.get('title') or not data.get('overview'):
                return None
            return {
                'tmdb_id': data['id'],
                'title': data['title'],
                'poster_path': data['poster_path'],
                'overview': data['overview'],
                'popularity': data['popularity'],
                'release_date': data.get('release_date'),  # 개봉일 포함
                'youtube_url': fetch_youtube_url(data['id'])  # YouTube URL 포함
            }
        return None
    except requests.RequestException:
        return None

def get_popular_movies():
    """TMDB API에서 인기 영화 목록 가져오기"""
    tmdb_api_key = settings.TMDB_API_KEY
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=ko-KR"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()['results']
        return []
    except requests.RequestException:
        return []

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
    today = datetime.now().date()
    cache_key = f'weather_{today}_{lat}_{lon}'
    cached_weather = cache.get(cache_key)
    
    if cached_weather:
        return cached_weather

    try:
        weather_api_key = settings.OPENWEATHER_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
        response = requests.get(url, timeout=5)
        weather_data = response.json()
        
        # 다음날 자정까지의 시간 계산
        tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
        cache_timeout = int((tomorrow - datetime.now()).total_seconds())
        cache.set(cache_key, weather_data, cache_timeout)
        
        return weather_data
    except requests.RequestException:
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

def get_movie_recommendation(weather, season, time_of_day, previous_tmdb_ids, holiday=None):
    if holiday:
        prompt = f"""오늘은 {holiday[0]}입니다. {holiday[1]} 관련 영화를 추천해주세요.
                    다음 TMDB ID를 가진 영화들은 제외해주세요: {', '.join(map(str, previous_tmdb_ids))}
                    TMDB ID로만 응답해주세요."""
        recommendation_type = "holiday"
    else:
        recommendation_type = random.choice(['weather', 'time'])
        if recommendation_type == 'weather':
            prompt = f"""날씨가 {weather}이고 {season}인 상황에 어울리는 영화를 추천해주세요.
                        다음 TMDB ID를 가진 영화들은 제외해주세요: {', '.join(map(str, previous_tmdb_ids))}
                        TMDB ID로만 응답해주세요."""
        else:
            prompt = f"""하루 중 {time_of_day} 시간대에 보기 좋은 영화를 추천해주세요.
                        다음 TMDB ID를 가진 영화들은 제외해주세요: {', '.join(map(str, previous_tmdb_ids))}
                        TMDB ID로만 응답해주세요."""

    response = client.chat.completions.create(
        model="gpt4o-mini",
        messages=[
            {"role": "system", "content": "당신은 영화 추천 전문가입니다. TMDB ID로만 응답해주세요."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        recommended_tmdb_id = int(response.choices[0].message.content.strip())
        return recommended_tmdb_id, recommendation_type
    except (ValueError, TypeError):
        return None, recommendation_type

def fetch_recommended_movies(weather, season, time_of_day, previous_tmdb_ids, holiday):
    today = datetime.now().date()
    cache_key = f'movie_recommendation_{today}_{hash(str(previous_tmdb_ids))}'
    cached_movie = cache.get(cache_key)
    
    if cached_movie:
        try:
            if isinstance(cached_movie, dict) and 'tmdb_id' in cached_movie:
                return cached_movie
        except (TypeError, AttributeError):
            cache.delete(cache_key)

    # 첫 번째 추천 시도
    recommended_tmdb_id, recommendation_type = get_movie_recommendation(
        weather, season, time_of_day, previous_tmdb_ids, holiday
    )

    # 첫 추천이 실패하면 최대 5번 더 시도
    attempts = 0
    while recommended_tmdb_id is None and attempts < 5:
        recommended_tmdb_id, recommendation_type = get_movie_recommendation(
            weather, season, time_of_day, previous_tmdb_ids, holiday
        )
        attempts += 1

    if recommended_tmdb_id:
        movie_data = get_tmdb_movie(recommended_tmdb_id)
        # 영화 데이터 검증 실패시 다시 시도
        attempts = 0
        while (movie_data is None) and (attempts < 5):
            recommended_tmdb_id, recommendation_type = get_movie_recommendation(
                weather, season, time_of_day, previous_tmdb_ids, holiday
            )
            if recommended_tmdb_id:
                movie_data = get_tmdb_movie(recommended_tmdb_id)
            attempts += 1

        if movie_data:
            result = (movie_data, recommendation_type)
            tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
            cache_timeout = int((tomorrow - datetime.now()).total_seconds())
            cache.set(cache_key, result, cache_timeout)
            return result

    return None, None

def fetch_popular_movie(previous_tmdb_ids, exclude_tmdb_id=None):
    """
    TMDB에서 인기 있는 영화 중 조건을 만족하는 최대 3개의 영화를 캐시에 저장하고,
    그 중 하나를 랜덤으로 반환. 속도를 개선하기 위해 캐싱을 적극 활용.
    """
    today = datetime.now().date()
    cache_key = f'popular_movies_{today}'  # 공통 캐싱 키
    cached_movies = cache.get(cache_key)

    # 캐싱된 데이터가 있으면 랜덤으로 하나 선택하여 반환
    if cached_movies:
        try:
            valid_movies = [
                movie for movie in cached_movies
                if movie['tmdb_id'] not in previous_tmdb_ids and movie['tmdb_id'] != exclude_tmdb_id
            ]
            if valid_movies:
                return random.choice(valid_movies)
        except (KeyError, AttributeError, IndexError):
            pass

    # TMDB API에서 인기 영화 목록 가져오기
    popular_movies = get_popular_movies()
    if not popular_movies:
        return None

    # 조건에 맞는 영화 저장
    valid_movies = []
    for movie in popular_movies:
        if len(valid_movies) >= 3:  # 최대 3개의 영화만 저장
            break

        # 이전 추천된 영화와 제외할 영화를 필터링
        if movie['id'] in previous_tmdb_ids or movie['id'] == exclude_tmdb_id:
            continue

        # TMDB ID로 영화 데이터 가져오기 및 성인물 필터링
        movie_data = get_tmdb_movie(movie['id'])
        if movie_data:  # 유효한 영화만 추가
            valid_movies.append(movie_data)

    # 유효한 영화가 있다면 캐싱하고 반환
    if valid_movies:
        # 캐싱 저장 (다음 날 자정까지 유효)
        tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
        cache_timeout = int((tomorrow - datetime.now()).total_seconds())
        cache.set(cache_key, valid_movies, cache_timeout)

        # 랜덤으로 하나 선택하여 반환
        return random.choice(valid_movies)

    return None

# def fetch_popular_movie(previous_tmdb_ids, exclude_tmdb_id=None):
#     today = datetime.now().date()
#     cache_key = f'popular_movie_{today}'
#     cached_movie = cache.get(cache_key)
    
#     if cached_movie:
#         try:
#             movie_id = cached_movie.get('tmdb_id', cached_movie.get('id'))
#             if movie_id and movie_id not in previous_tmdb_ids:
#                 return cached_movie
#         except (KeyError, AttributeError):
#             pass

#     popular_movies = get_popular_movies()
#     if not popular_movies:  # API 요청 실패시 재시도
#         attempts = 0
#         while not popular_movies and attempts < 3:
#             popular_movies = get_popular_movies()
#             attempts += 1
    
#     # 이전에 선택한 영화와 제외할 영화를 필터링
#     available_movies = [
#         movie for movie in popular_movies 
#         if movie['id'] not in previous_tmdb_ids 
#         and movie['id'] != exclude_tmdb_id
#     ]
    
#     # 사용 가능한 영화들을 순회하면서 적절한 영화 찾기
#     for movie in available_movies:
#         movie_data = get_tmdb_movie(movie['id'])
#         if movie_data:  # 성인물이 아니고 한국어 정보가 있는 영화를 찾으면
#             try:
#                 tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
#                 cache_timeout = int((tomorrow - datetime.now()).total_seconds())
#                 cache.set(cache_key, movie_data, cache_timeout)
#                 return movie_data
#             except Exception:
#                 continue
    
#     # 여전히 적절한 영화를 찾지 못했다면, 다른 페이지의 인기 영화 시도
#     if not movie_data:
#         for page in range(2, 4):  # 2~3 페이지까지 시도
#             try:
#                 url = f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=ko-KR&page={page}"
#                 response = requests.get(url, timeout=5)
#                 if response.status_code == 200:
#                     next_page_movies = response.json()['results']
#                     available_movies = [
#                         movie for movie in next_page_movies 
#                         if movie['id'] not in previous_tmdb_ids 
#                         and movie['id'] != exclude_tmdb_id
#                     ]
                    
#                     for movie in available_movies:
#                         movie_data = get_tmdb_movie(movie['id'])
#                         if movie_data:
#                             try:
#                                 tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time())
#                                 cache_timeout = int((tomorrow - datetime.now()).total_seconds())
#                                 cache.set(cache_key, movie_data, cache_timeout)
#                                 return movie_data
#                             except Exception:
#                                 continue
#             except requests.RequestException:
#                 continue
    
#     return None