<template>
  <div class="container">
    <div class="logo">
    <i class="fas fa-film"></i>
    <span class="logo-text">MIYH*</span>
  </div>
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
import { useCounterStore } from '@/stores/counter';

const router = useRouter();
const store = useCounterStore();

const login = function () {
  router.push({ name: 'login' }); 
};

const signup = function () {
  router.push({ name: 'signup' }); 
};

const kakaoLogin = async () => {
  // store의 kakaoLogin 함수 호출
  try {
    await store.kakaoLogin();
  } catch (error) {
    console.error('카카오 로그인 실패:', error);
    alert('카카오 로그인에 실패했습니다.');
  }
};
</script>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  animation: fadeIn 0.5s ease-in;
}

.fa-film {
  font-size: 2.5rem;
  color: #e31c1c;
  transform: rotate(-15deg);
  transition: transform 0.3s ease;
}

.logo:hover .fa-film {
  transform: rotate(0deg);
}

.logo-text {
  font-size: 2.8rem;
  font-weight: 700;
  color: red;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  font-family: 'Arial', sans-serif;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 480px) {
  .fa-film {
    font-size: 2rem;
  }
  
  .logo-text {
    font-size: 2.2rem;
  }
}
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

.kakao-btn {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #FEE500;
  color: #000000;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.kakao-btn:hover {
  background-color: #FDD835;
}

.kakao-icon {
  width: 24px;
  height: 24px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 300px;
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