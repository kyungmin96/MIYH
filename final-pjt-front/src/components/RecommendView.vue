<template>
  <div class="movie-card" v-if="movieData" @click="goToMovieDetail">
    <div class="card-header">
      <h2>오늘의 추천 영화</h2>
    </div>
    <div class="card-content" v-if="movieData">
      <div class="poster-container">
        <img :src="getImageUrl(movieData.poster_path)" alt='No'>
      </div>
      <div class="movie-info">
        <h3 class="movie-title">{{ movieData.title }}</h3>
        <p class="movie-overview">{{ truncateOverview(movieData.overview) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
  movieData: {
    type: Object,
    required: true
  }
})

const getImageUrl = (posterPath) => {
  return `https://image.tmdb.org/t/p/original${posterPath}`
}

const truncateOverview = (text) => {
  if (!text) return '';
  return text.length > 200 ? text.slice(0, 200) + '...' : text;
}

const goToMovieDetail = () => {
  router.push(`/movie/${props.movieData.movie_id}`)
}
</script>

<style scoped>
.movie-card {
  background: #242937;
  border-radius: 12px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  width: 100%;
  height: 400px; /* 고정 높이 설정 */
  display: flex;
  flex-direction: column;
  cursor: pointer; /* 커서 스타일 추가 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
.card-header {
  margin-bottom: 20px;
}

.card-header h2 {
  color: #ffffff;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  padding-bottom: 10px;
  border-bottom: 2px solid #dc1a28;
}

.card-content {
  display: flex;
  gap: 25px;
  flex: 1;
  overflow: hidden;
}

.poster-container {
  flex-shrink: 0;
  width: 200px;
}

img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

img:hover {
  transform: scale(1.05);
}

.movie-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.movie-title {
  color: #ffffff;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  letter-spacing: -0.02em;
}

.movie-overview {
  color: #a0a0a0;
  font-size: 0.95rem;
  line-height: 1.6;
  letter-spacing: -0.01em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 8;
  -webkit-box-orient: vertical;
}

@media (max-width: 768px) {
  .movie-card {
    height: auto;
    min-height: 600px;
  }

  .card-content {
    flex-direction: column;
    align-items: center;
  }
  
  .movie-info {
    text-align: center;
  }
  
  .movie-overview {
    -webkit-line-clamp: 6;
  }
}
</style>