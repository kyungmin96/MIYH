<template>
  <div class="signup-container">
    <div class="signup-box">
      <div class="signup-header">
        <i class="fas fa-film"></i>
        <h1>회원가입</h1>
        <p class="subtitle">MIYH와 함께 새로운 영화의 세계로</p>
      </div>

      <form @submit.prevent="signUp">
        <div class="form-group">
          <label for="username">아이디</label>
          <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input type="text" id="username" v-model.trim="username" placeholder="ID를 입력하세요.">
          </div>
        </div>

        <div class="form-group">
          <label for="password1">비밀번호</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input type="password" id="password1" v-model.trim="password1" placeholder="영문, 숫자 포함 8자 이상">
          </div>
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input type="password" id="password2" v-model.trim="password2" placeholder="영문, 숫자 포함 8자 이상">
          </div>
        </div>

        <div class="form-group">
          <label for="name">이름</label>
          <div class="input-wrapper">
            <i class="fas fa-id-card"></i>
            <input type="text" id="name" v-model.trim="name" placeholder="닉네임을 입력해주세요.">
          </div>
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope"></i>
            <input type="email" id="email" v-model.trim="email" placeholder="중복되지 않은 이메일을 사용해 주세요.">
          </div>
        </div>

        <button type="submit" class="signup-btn">회원가입</button>
      </form>

      <div class="login-link">
        <span>이미 계정이 있으신가요?</span>
        <button @click="login" class="login-btn">로그인</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router';
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email =ref(null)
const name =ref(null)
const router = useRouter()
const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    name: name.value,
    email:email.value
  }
  store.signUp(payload)
}
const login = function () {
  router.push({ name: 'login'}) 
}
</script>

<style scoped>
.signup-container {
  min-height: 100vh;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
}

.signup-box {
  width: 100%;
  height: 88%;
  max-width: 480px;
  background: rgba(28, 33, 46, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.signup-header {
  text-align: center;
  margin-bottom: 40px;
}

.signup-header i {
  font-size: 40px;
  color: #e50914;
  margin-bottom: 20px;
}

h1 {
  color: #ffffff;
  font-size: 2rem;
  margin-bottom: 10px;
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

.signup-btn {
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

.signup-btn:hover {
  background: #f40612;
  transform: translateY(-2px);
}

.login-link {
  text-align: center;
  margin-top: 24px;
  color: #b3b3b3;
}

.login-btn {
  background: none;
  border: none;
  color: #e50914;
  font-weight: 600;
  cursor: pointer;
  margin-left: 8px;
  transition: all 0.3s ease;
}

.login-btn:hover {
  color: #f40612;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .signup-box {
    padding: 30px 20px;
  }

  h1 {
    font-size: 1.8rem;
  }
}
</style>