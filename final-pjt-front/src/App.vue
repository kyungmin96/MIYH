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
    <nav v-if="isLoggedIn" class="header-nav">
      <div class="nav-container">
        <!-- 로고를 RouterLink로 변경 -->
        <RouterLink 
          v-if="userName" 
          :to="{name:'calender', params: { userName: userName }}" 
          class="nav-brand"
        >
          <i class="fas fa-film"></i>
          <span>MIYH</span>
        </RouterLink>
        
        <div class="nav-links">
          <!-- Home 링크 제거 -->
          <RouterLink 
            v-if="userName" 
            :to="{name:'mypage', params: { userName: userName }}" 
            class="nav-item"
          >
            <i class="fas fa-user"></i>
            MyPage
          </RouterLink>
          <RouterLink :to="{name:'movie'}" class="nav-item">
            <i class="fas fa-video"></i>
            Movie
          </RouterLink>
          <RouterLink :to="{name:'article'}" class="nav-item">
            <i class="fas fa-comments"></i>
            게시판
          </RouterLink>
        </div>
        <button @click="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          로그아웃
        </button>
      </div>
    </nav>

    <main :class="{ 'main-content': isLoggedIn, 'main-content-logout': !isLoggedIn }">
      <RouterView />
    </main>
  </div>
</template>
<style>
:root {
  --bg-primary: #0f1117;
  --bg-secondary: #161b26;
  --nav-bg: rgba(22, 27, 34, 0.95);
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
  --accent-color: #e50914;
  --accent-hover: #f40612;
  --border-color: rgba(255, 255, 255, 0.1);
}

html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  overflow-x: hidden;
  background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
  color: var(--text-primary);
  font-family: 'Noto Sans KR', sans-serif;
}

.app-container {
  min-height: 100vh;

  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.header-nav {
  position: sticky;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background: var(--nav-bg);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  border-bottom: 1px solid var(--border-color);
}

.nav-container {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--accent-color);
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
}

.nav-brand i {
  font-size: 1.8rem;
}
.nav-brand:hover {
  transform: translateY(-2px);
  color: var(--accent-hover);
}
.nav-links {
  display: flex;
  gap: 2rem;
}
.nav-brand.router-link-active {
  color: var(--accent-color);
}

.nav-item {
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-item:hover {
  color: var(--text-primary);
  transform: translateY(-2px);
}

.nav-item.router-link-active {
  color: var(--accent-color);
  position: relative;
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--accent-color);
  box-shadow: 0 0 10px var(--accent-color);
}

.logout-btn {
  padding: 0.8rem 1.5rem;
  background: var(--accent-color);
  color: var(--text-primary);
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3);
}

.main-content-logout {
  position: fixed;  /* absolute를 fixed로 변경 */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* min-height를 height로 변경 */
  width: 100vw; /* 100%를 100vw로 변경 */
  overflow: hidden; /* 오버플로우 방지 */
  background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
}

.main-content {
  flex: 1;
  min-height: calc(100vh - 70px);
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
  }

  .nav-brand span {
    display: none;
  }

  .nav-links {
    gap: 1rem;
  }

  .nav-item {
    padding: 0.5rem;
  }

  .nav-item span {
    display: none;
  }

  .logout-btn {
    padding: 0.6rem 1rem;
  }

  .logout-btn span {
    display: none;
  }
}
</style>