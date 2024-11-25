<template>
  <div class="movie-list">
    <div class="search-container">
      <form @submit.prevent="searchMovies" class="search-form">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="영화 제목을 입력하세요"
          class="search-input"
        >
        <button type="submit" class="search-btn">
          <i class="fas fa-search"></i>
          검색
        </button>
      </form>
    </div>

    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      <span>영화 목록을 불러오는 중...</span> 
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
import { useCounterStore } from '@/stores/counter';

const searchQuery = ref('');
const loading = ref(true);
const movies = ref([]);
const store = useCounterStore();
const originalMovies = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get(`${store.API_URL}/community/movies/`);
    movies.value = response.data;
    originalMovies.value = [...response.data];
  } catch (error) {
    console.error('영화 데이터 로드 실패:', error);
  } finally {
    loading.value = false;
  }
});

const searchMovies = async () => {
  if (!searchQuery.value.trim()) {
    movies.value = originalMovies.value;
    return;
  }
  
  loading.value = true;
  try {
    const response = await axios.get(
      `${store.API_URL}/community/movies/search/?query=${encodeURIComponent(searchQuery.value.trim())}`
    );
    movies.value = response.data;
    console.log(movies)
  } catch (error) {
    console.error('영화 검색 실패:', error);
    // 검색 실패시 원본 데이터 유지
    movies.value = originalMovies.value;
  } finally {
    loading.value = false;
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.movie-list {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
  font-family: var(--font-primary);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #a0a0a0;
  gap: 15px;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
}

.loading i {
  font-size: 2rem;
  color: #dc1a28;
}

.movies-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 20px 0;
}

.search-container {
  margin-bottom: 30px;
}

.search-form {
  display: flex;
  gap: 10px;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 12px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  background: #242937;
  color: #ffffff;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
}

.search-input:focus {
  outline: none;
  background: #2d3340;
  box-shadow: 0 0 0 2px rgba(220, 26, 40, 0.5);
}

.search-btn {
  padding: 12px 24px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
}

.search-btn:hover {
  background: #b91521;
  transform: translateY(-2px);
}

.search-btn i {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    padding: 0 15px;
  }

  .search-input,
  .search-btn {
    width: 100%;
  }

  .movie-list {
    padding: 0 15px;
  }

  .movies-container {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }
}
</style>