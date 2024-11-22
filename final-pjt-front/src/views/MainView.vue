<template>
  <div class="container">
    <div class="title">
      오늘의 영화를 추가하세요!
    </div>
    <div class="button-group">
      <button class="primary-btn" @click="login">로그인하기</button>
      <button class="secondary-btn" @click="signup">회원 가입</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()

const login = function () {
  router.push({ name: 'login'}) 
}

const signup = function () {
  router.push({ name: 'signup'}) 
}
</script>

<style scoped>
.container {
  background-color: #1a1f2c;
  height: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
  text-align: center;
  padding: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 2rem;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 300px;
}

.primary-btn, .secondary-btn {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn {
  background-color: #e31c1c;
  color: white;
}

.primary-btn:hover {
  background-color: #c41818;
}

.secondary-btn {
  background-color: #2c3e50;
  color: white;
}

.secondary-btn:hover {
  background-color: #34495e;
}

@media (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }
  
  .button-group {
    max-width: 250px;
  }
}
</style>