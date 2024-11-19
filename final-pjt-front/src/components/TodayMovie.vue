<template>
  <div class="today-movie">
    <h1>오늘의 선택 영화</h1>
    <div class="movie-content">
      <img :src="poster" alt="영화 포스터 1">
    </div>
  </div>
</template>

<script setup>
import poster2 from '../image/TMY-698.jpg'

const poster = poster2
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