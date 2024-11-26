<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <i class="fas fa-film"></i>
        <h1>MIYH</h1>
        <p class="subtitle">영화와 함께하는 특별한 순간</p>
      </div>

      <form @submit.prevent="logIn">
        <div class="form-group">
          <label for="username">아이디</label>
          <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input 
              type="text" 
              id="username" 
              autocomplete="username" 
              v-model.trim="username"
              placeholder="아이디를 입력하세요"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input 
              type="password" 
              id="password" 
              autocomplete="current-password" 
              v-model.trim="password"
              placeholder="비밀번호를 입력하세요"
            >
          </div>
        </div>

        <button type="submit" class="login-btn">로그인</button>
      </form>

      <div class="signup-link">
        <span>아직 계정이 없으신가요?</span>
        <button @click="signUp" class="signup-btn">회원가입</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password = ref(null)
const router = useRouter()
const store = useCounterStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
const signUp = function () {
  router.push({ name: 'signup'}) 
}

</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
}

.login-box {
  width: 100%;
  max-width: 420px;
  background: rgba(28, 33, 46, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header i {
  font-size: 40px;
  color: #e50914;
  margin-bottom: 20px;
}

h1 {
  color: #ffffff;
  font-size: 2.2rem;
  margin-bottom: 10px;
  letter-spacing: 2px;
}

.subtitle {
  color: #b3b3b3;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  color: #ffffff;
  margin-bottom: 8px;
  font-size: 0.9rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: 12px;
  color: #b3b3b3;
}

input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

input::placeholder {
  color: #666;
}

input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(229, 9, 20, 0.5);
  outline: none;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.login-btn:hover {
  background: #f40612;
  transform: translateY(-2px);
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  color: #b3b3b3;
}

.signup-btn {
  background: none;
  border: none;
  color: #e50914;
  font-weight: 600;
  cursor: pointer;
  margin-left: 8px;
  transition: all 0.3s ease;
}

.signup-btn:hover {
  color: #f40612;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }

  h1 {
    font-size: 1.8rem;
  }

  .login-btn {
    padding: 12px;
  }
}
</style>