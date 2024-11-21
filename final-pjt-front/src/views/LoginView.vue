<template>
  <div class="login-container">
    <h1>LogIn Page</h1>
    <form @submit.prevent="logIn">
      <label for="username">ID : </label>
      <input type="text" id="username" autocomplete="username" v-model.trim="username"><br>

      <label for="password">password : </label>
      <input type="password" id="password" autocomplete="current-password" v-model.trim="password"><br>

      <input type="submit" value="logIn">
    </form>
      <button @click="signUp">회원가입 하러 가기</button>
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  text-align: center;
}

form {
  background: #ffffff;
  padding: 2rem 3rem;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #34495e;
  font-weight: 500;
  font-size: 1rem;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

input[type="submit"] {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  background-color: #3498db;
  color: white;
  margin: 1rem 0;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #2980b9;
}

button {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  background-color: #2ecc71;
  color: white;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #27ae60;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-container {
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
  input[type="submit"],
  button {
    padding: 0.6rem;
  }
}
</style>
