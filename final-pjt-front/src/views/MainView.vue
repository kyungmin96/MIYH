<template>
  <div class="container">
    <div>
      오늘의 영화를 추가하세요!
    </div>
    <div>
      <button @click="login">로그인하기</button>
    </div>
    <div>
      <button @click="signup">회원 가입</button>
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
  padding: 2rem;
  text-align: center;
  background-color: #1a1a1a; /* 어두운 배경 */
}

div:first-child {
  font-size: 2.5rem;
  font-weight: bold;
  color: #ffffff; /* 밝은 텍스트 */

  padding: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

button {
  width: 250px;
  padding: 1rem;
  margin: 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

button:first-of-type {
  background-color: #4a90e2; /* 로그인 버튼 */
  color: white;
}

button:first-of-type:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

button:last-of-type {
  background-color: #50c878; /* 회원가입 버튼 */
  color: white;
}

button:last-of-type:hover {
  background-color: #3ca25f;
  transform: translateY(-2px);
}

@media (max-width: 480px) {
  div:first-child {
    font-size: 1.8rem;
  }

  button {
    width: 80%;
    max-width: 250px;
  }
}
</style>