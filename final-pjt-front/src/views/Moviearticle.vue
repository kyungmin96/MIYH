<template>
  <div>
    <h1>영화 목록</h1>
    <MovieList />
  </div>
</template>

<script setup>
import MovieList from '@/components/MovieList.vue';


</script>

<style scoped>
h1 {
  font-size: 2.5rem;
  color: #ffffff;
  text-align: center;
  margin: 2rem 0;
  padding: 1rem;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: linear-gradient(to right, transparent, #4a90e2, transparent);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
    margin: 1.5rem 0;
    letter-spacing: 2px;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.8rem;
    margin: 1rem 0;
    letter-spacing: 1px;
  }
}
</style>