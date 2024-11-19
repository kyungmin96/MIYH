<template>
  <div class="recommend-container">
    <div>영화 제목</div>
    <img :src="poster1Url" alt="영화 포스터 1">
  </div>
</template>

<script setup>
import poster1 from '../image/TMZ-223.jpg'


// 변수명 충돌을 피하기 위해 다른 이름으로 선언
const poster1Url = poster1

</script>

<style scoped>
img {
  width: 200px;
  height: auto;
  object-fit: cover;
}
.recommend-container{
  width: 50%;
}
</style>