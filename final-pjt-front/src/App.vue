<script setup>
import { RouterLink, RouterView } from 'vue-router'
const userId=1
</script>

<template>
  <div class="app-container">
    <nav class="header-nav">
      <div class="nav-container">
        <RouterLink :to="{name:'calender', params: { id: userId }}" class="nav-item">Home</RouterLink>
        <RouterLink :to="{name:'mypage', params: { id: userId }}" class="nav-item">MyPage</RouterLink>
        <RouterLink :to="{name:'login'}" class="nav-item">Services</RouterLink>
        <RouterLink :to="{name:'signup'}" class="nav-item">Contact</RouterLink>
        <RouterLink :to="{name:'movie'}" class="nav-item">Movie</RouterLink>
      </div>
    </nav>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* 전역 스타일 추가 */
html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  overflow-x: hidden;
}

/* 스코프된 스타일 */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.header-nav {
  position: sticky; /* fixed에서 sticky로 변경 */
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.nav-item {
  text-decoration: none;
  color: #333333;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: #007bff;
}

.nav-item.router-link-active {
  color: #007bff;
  border-bottom: 2px solid #007bff;
}

.main-content {
  flex: 1;
  width: 100%;
  height: calc(100vh - 60px);
  overflow-y: auto; /* 스크롤이 필요한 경우에만 표시 */
  box-sizing: border-box;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .header-nav {
    height: 50px;
  }

  .nav-container {
    padding: 0 1rem;
  }

  .nav-item {
    padding: 0.5rem;
    font-size: 0.9rem;
  }

  .main-content {
    height: calc(100vh - 50px);
  }
}
</style>