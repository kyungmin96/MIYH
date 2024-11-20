<template>
<div class="movie-item" @click="goToDetail">
    <div class="movie-image">
      <img :src="movie.poster_url
" :alt="movie.title">
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
.movie-item {
  display: flex;
  border: 1px solid #333;
  border-radius: 12px;
  overflow: hidden;
  background: #1a1a1a;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  transition: transform 0.3s ease;
  margin-bottom: 20px;
  cursor: pointer;
}

.movie-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

.movie-image {
  flex: 0 0 200px; /* 이미지 너비 고정 */
  position: relative;
}

.movie-image img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-info {
  flex: 1;
  padding: 20px;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.movie-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.4rem;
  color: #fff;
  font-weight: 600;
}

.movie-info p {
  margin: 0;
  color: #ccc;
  font-size: 1rem;
  line-height: 1.6;
}

.movie-rating {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0,0,0,0.7);
  color: #ffd700;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9rem;
  z-index: 1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .movie-item {
    flex-direction: column;
  }

  .movie-image {
    flex: none;
    width: 100%;
  }

  .movie-image img {
    height: 200px;
  }

  .movie-info h3 {
    font-size: 1.2rem;
  }

  .movie-info p {
    font-size: 0.9rem;
  }
}
</style>