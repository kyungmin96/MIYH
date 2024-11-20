<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useCounterStore()

// optional chaining을 사용하여 안전하게 접근
const userId = computed(() => store.currentUser?.pk)
const userName = computed(() => store.currentUser?.username)
const isLoggedIn = computed(() => !!store.token)

// 로그아웃 함수
const logout = async () => {
  await store.logOut() // store의 logOut 함수가 Promise를 반환한다고 가정
  sessionStorage.clear()
  router.push({ name: 'home' })
}

// 브라우저 창이 완전히 닫힐 때만 실행
window.addEventListener('unload', () => {
  localStorage.clear()
})
</script>

<template>
  <div class="app-container">
    <!-- 로그인 상태일 때만 헤더 표시 -->
    <nav v-if="isLoggedIn" class="header-nav">
      <div class="nav-container">
        <RouterLink 
          v-if="userId" 
          :to="{name:'calender', params: { id: userId }}" 
          class="nav-item"
        >
          Home
        </RouterLink>
        <RouterLink 
          v-if="userName" 
          :to="{name:'mypage', params: { name: userName }}" 
          class="nav-item"
        >
          MyPage
        </RouterLink>
        <RouterLink :to="{name:'movie'}" class="nav-item">Movie</RouterLink>
        <RouterLink :to="{name:'article'}" class="nav-item">게시판</RouterLink>
        <button @click="logout" class="logout-btn">로그아웃</button>
      </div>
    </nav>

    <!-- 메인 컨텐츠 영역 -->
    <main :class="{ 'main-content': isLoggedIn, 'main-content-logout': !isLoggedIn }">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* 기존 스타일 유지하고 아래 스타일 추가/수정 */

/* 로그아웃 버튼 스타일 추가 */
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
  background-color: #ffffff; /* 배경색 추가 */
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
.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #c82333;
  transform: translateY(-2px);
}
.main-content-logout {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  /* background-color: #333333; */
  color: white;
}

/* 로그인 상태일 때의 main-content 스타일 */
.main-content {
  flex: 1;
  min-height: calc(100vh - 60px); /* 헤더 높이를 뺀 나머지 */
}

@media (max-width: 768px) {
  .main-content {
    height: calc(100vh - 50px);
  }

}
</style>