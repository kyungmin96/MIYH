<template>
  <div class="movie-item" @click="goToDetail">
    <div class="movie-image">
      <img :src="movie.poster_url" :alt="movie.title">
      <div class="movie-overlay">
        <span class="view-details">
          <i class="fas fa-info-circle"></i>
          상세보기
        </span>
      </div>
    </div>
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
      <p>{{ movie.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const goToDetail = () => {
  router.push({ name: 'movie-detail', params: { id: props.movie.id }})
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.movie-item {
  background: #1a1f2c;
  height: 450px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  font-family: var(--font-primary);
}

.movie-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.movie-image {
  position: relative;
  width: 100%;
  height: 85%; /* 75%에서 85%로 증가 */
}

.movie-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.movie-item:hover .movie-overlay {
  opacity: 1;
}

.view-details {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.02em;
}

.view-details i {
  font-size: 1.2rem;
  color: #dc1a28;
}

.movie-info {
  height: 15%; /* 25%에서 15%로 감소 */
  width: 100%;
  padding: 10px 15px; /* 상하 패딩 감소 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.movie-info h3 {
  color: #ffffff;
  font-size: 1.1rem; /* 글자 크기 약간 감소 */
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.03em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.movie-info p {
  color: #a0a0a0;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-top: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  letter-spacing: -0.01em;
}

@media (max-width: 768px) {
  .movie-image {
    height: 80%; /* 모바일에서도 이미지 비율 증가 */
  }

  .movie-info {
    height: 20%;
  }

  .movie-info h3 {
    font-size: 1rem;
  }


  .movie-info p {
    font-size: 0.85rem;
    -webkit-line-clamp: 1;
  }
}
</style>