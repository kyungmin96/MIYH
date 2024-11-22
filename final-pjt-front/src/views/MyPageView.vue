<template>
  <div class="profile-container" v-if="profileData">
    <div class="profile-header">
      <div class="profile-avatar">
        <span>{{ profileData.name.charAt(0).toUpperCase() }}</span>
      </div>
      <div class="profile-info">
        <h1>{{ profileData.name }} 님의 프로필</h1>
        <div class="follow-stats">
          <div class="stat-item">
            <i class="fas fa-users"></i>
            <span>팔로워 {{ profileData.followers_count }}명</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-user-friends"></i>
            <span>팔로잉 {{ profileData.followings_count }}명</span>
          </div>
        </div>
        <div class="profile-actions">
          <button 
            v-if="profileData.username !== store.currentUser?.username"
            @click="toggleFollow" 
            :class="['follow-btn', { 'following': isFollowing }]"
          >
            <i :class="isFollowing ? 'fas fa-user-minus' : 'fas fa-user-plus'"></i>
            {{ isFollowing ? '팔로우 취소' : '팔로우' }}
          </button>
          <button @click="gocalender" class="calendar-btn">
            <i class="fas fa-calendar-alt"></i>
            캘린더 보기
          </button>
        </div>
      </div>
    </div>
    
    <div class="list-container">
      <WriteList :profileData="profileData" />
      <FollowerList :profileData="profileData" />
      <FollowingList :profileData="profileData"/>
    </div>
  </div>
  <div v-else class="loading-container">
    <div class="loading-spinner"></div>
    <span>프로필을 불러오는 중...</span>
  </div>
</template>

<script setup>
import WriteList from '@/components/WriteList.vue';
import { ref, watch, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';
import FollowingList from '@/components/FollowingList.vue'; 
import FollowerList from '@/components/FollowerList.vue'
import axios from 'axios';

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const profileData = ref(null)
const isFollowing = ref(false)
// 프로필 정보 가져오기
const fetchProfile = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/v1/accounts/profile/${route.params.userName}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    profileData.value = response.data
    isFollowing.value = response.data.is_followed
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    if (error.response?.status === 404) {
      alert('존재하지 않는 사용자입니다.')
      router.go(-1) // 이전 페이지로 돌아가기
    }
  }
}
watch(
  () => route.params.userName,
  async (newUserName, oldUserName) => {
    if (newUserName && newUserName !== oldUserName && store.token) {
      await fetchProfile(newUserName)
    }
  },
  { immediate: true }
)

// 팔로우/언팔로우 토글
const toggleFollow = async () => {
  try {
    const response = await axios({
      method: 'POST',
      url: `http://127.0.0.1:8000/api/v1/accounts/profile/${route.params.userName}/follow/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    
    // 팔로우 상태 및 카운트 업데이트
    isFollowing.value = !isFollowing.value
    profileData.value.followers_count += isFollowing.value ? 1 : -1
  } catch (error) {
    console.error('팔로우 토글 실패:', error)
    alert('팔로우 처리 중 오류가 발생했습니다.')
  }
}

// onMounted 훅 수정
onMounted(async () => {
  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  await fetchProfile()
})

const gocalender = () => {
  router.push({
    name: 'calender',
    params: { userName: route.params.userName }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');
:root {
  /* 기존 변수들 */
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.profile-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
  font-family: var(--font-primary);
}

.profile-header {
  background: #1a1f2c;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 25px;
  margin-bottom: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  letter-spacing: -0.02em;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #dc1a28, #9e0f19);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: bold;
  font-family: var(--font-secondary);
  font-weight: 600;
}

.profile-info {
  flex: 1;
}

.profile-info h1 {
  margin: 0 0 12px 0;
  color: #ffffff;
  font-size: 1.6rem;
  font-family: var(--font-primary);
  font-weight: 700;
  letter-spacing: -0.03em;
}

.follow-stats {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #a0a0a0;
  font-size: 0.95rem;
  font-family: var(--font-primary);
  font-weight: 500;
  letter-spacing: -0.01em;
}

.stat-item i {
  color: #dc1a28;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.follow-btn {
  padding: 8px 18px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #dc1a28;
  color: white;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.follow-btn.following {
  background: #2d3340;
  border: 1px solid #dc1a28;
}

.follow-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.calendar-btn {
  padding: 8px 18px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #2d3340;
  color: white;
  transition: all 0.2s ease;
  border: 1px solid rgba(220, 26, 40, 0.5);
  font-family: var(--font-primary);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.calendar-btn i {
  color: #dc1a28;
}

.calendar-btn:hover {
  background: #363d4d;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.list-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  gap: 12px;
  color: #a0a0a0;
  font-family: var(--font-primary);
  font-weight: 500;
  letter-spacing: -0.01em;
}

.loading-spinner {
  width: 35px;
  height: 35px;
  border: 3px solid #2d3340;
  border-top: 3px solid #dc1a28;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .list-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .follow-stats {
    flex-direction: column;
    gap: 12px;
  }

  .profile-actions {
    flex-direction: column;
    width: 100%;
  }

  .calendar-btn {
    width: 100%;
    justify-content: center;
  }

  .list-container {
    grid-template-columns: 1fr;
  }
}
</style>