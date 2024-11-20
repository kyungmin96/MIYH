<template>
  <div class="movie-list">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else class="movies-container">
      <MovieListItem
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import MovieListItem from '@/components/MovieListItem.vue';

const loading = ref(true);
const movies = ref([])
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/movies/');
    movies.value = response.data;
    console.log('영화 데이터 로드 완료:', response.data);
  } catch (error) {
    console.error('영화 데이터 로드 실패:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.movie-list {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 1.2rem;
  color: #666;
}

.movies-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
</style>