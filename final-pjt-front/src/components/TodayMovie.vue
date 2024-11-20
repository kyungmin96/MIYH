<template>
  <div class="today-movie">
    <h1>오늘의 영화</h1>
    <div v-if="todayMovie" class="movie-content">
      <img :src="todayMovie.img" :alt="todayMovie.title">
    </div>
    <div v-else class="no-movie">
      오늘 등록된 영화가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

// 오늘 날짜 구하기
const getCurrentDate = () => {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 오늘 날짜의 영화 찾기
const todayMovie = computed(() => {
  const today = getCurrentDate();
  const event = store.events.find(event => event.start === today);
  if (event) {
    return store.movies.find(movie => movie.id === event.extendedProps.movieId);
  }
  return null;
});

</script>

<style scoped>
.today-movie {
  width: 33%;
  height: 40vh; /* 이전 컴포넌트와 동일한 높이 */
  border: 1px solid #ccc;
  padding: 15px;
}

.movie-content {
  height: calc(80% - 50px); /* h1 높이를 고려하여 조정 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.movie-content img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 이미지 비율 유지 */
  border-radius: 4px; /* 선택사항: 이미지 모서리 둥글게 */
}
</style>