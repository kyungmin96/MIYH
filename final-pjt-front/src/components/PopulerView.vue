<template>
 <div class="populer-container">
    <div>영화 제목</div>
    <img :src="poster2Url" alt="영화 포스터 1">
  </div>
</template>

<script setup>

import poster2 from '../image/TMY-104.jpg'

// 변수명 충돌을 피하기 위해 다른 이름으로 선언

const poster2Url = poster2
</script>

<style scoped>
img {
  width: 200px;
  height: auto;
  object-fit: cover;
}
.populer-container{
  width: 50%;
  
}
</style>