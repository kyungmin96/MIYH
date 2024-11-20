<template>
  <div class="signup-container">
    <h1>SignUp Page</h1>
    <form @submit.prevent="signUp">
  <div class="form-group">
    <label for="username">ID : </label>
    <input type="text" id="username" v-model.trim="username" placeholder="영문, 숫자 포함 4-12자">
  </div>

  <div class="form-group">
    <label for="password1">password : </label>
    <input type="password" id="password1" v-model.trim="password1" placeholder="영문, 숫자 포함 4-12자">
  </div>

  <div class="form-group">
    <label for="password2">password confirmation : </label>
    <input type="password" id="password2" v-model.trim="password2">
  </div>

  <div class="form-group">
    <label for="name">username : </label>
    <input type="text" id="name" v-model.trim="name" placeholder="영문, 숫자 포함 4-12자">
  </div>

  <div class="form-group">
    <label for="email">email : </label>
    <input type="email" id="email" v-model.trim="email" placeholder="중복되지 않은 이메일을 사용해 주세요.">
  </div>
  
  <input type="submit" value="SignUp">
</form>
    <div>
      <button @click="login">로그인 하러 가기</button>
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
  min-height: calc(100vh - 60px);
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  text-align: center;
}

form {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem 3rem;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1.5rem;
  width: 100%;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #34495e;
  font-weight: 500;
  font-size: 1rem;
}

input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="password"]:focus,
input[type="email"]:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

input[type="submit"] {
  width: 100%;
  padding: 0.8rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin: 1rem 0;
}

input[type="submit"]:hover {
  background-color: #2980b9;
}

button {
  width: 100%;
  padding: 0.8rem;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1rem;
}

button:hover {
  background-color: #27ae60;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .signup-container {
    padding: 10px;
  }

  form {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  input[type="text"],
  input[type="password"],
  input[type="email"],
  input[type="submit"],
  button {
    padding: 0.6rem;
  }
}
</style>