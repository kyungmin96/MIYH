<template>
  <div class="profile-container" v-if="profileData">
    <div class="profile-name">
      <h1>{{ profileData.username }} 님의 프로필</h1>
      <div class="follow-section">
        <span>팔로워 수: {{ profileData.followers_count }}</span>
        <span>팔로잉 수: {{ profileData.followings_count }}</span>
        <button 
          @click="toggleFollow" 
          :class="{ 'following': isFollowing }"
          v-if="profileData.username !== store.currentUser?.username"
        >
          {{ isFollowing ? '팔로우 취소' : '팔로우' }}
        </button>
      </div>
    </div>
    <div class="list-con">
      <!-- profileData 전체를 props로 전달 -->
      <WriteList :profileData="profileData" />
      <!-- <FollowerList :profileData="profileData" /> -->
      <FollowingList :folloinglist="folloinglist"/>
    </div>
  </div>
  <div v-else class="loading">
    Loading...
  </div>
</template>

<script setup>
import WriteList from '@/components/WriteList.vue';
import { ref, watch, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';
import FollowerList from '@/components/FollowerList.vue'
import axios from 'axios';
import FollowingList from '@/components/FollowingList.vue';  // 한 번만 import

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const profileData = ref(null)
const isFollowing = ref(false)
const folloinglist = ref([])
// 프로필 정보 가져오기
const fetchProfile = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/accounts/profile/${route.params.name}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    profileData.value = response.data
    isFollowing.value = response.data.is_followed
    console.log('프로필 데이터:', response.data)
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    if (error.response?.status === 404) {
      alert('존재하지 않는 사용자입니다.')
      router.push('/')
    }
  }
}
watch(
  () => route.params.name,
  async (newName) => {
    if (newName && store.token) {
      await fetchProfile()
    }
  }
)

// 팔로우/언팔로우 토글
const toggleFollow = async () => {
  try {
    const response = await axios({
      method: 'POST',
      url: `http://127.0.0.1:8000/api/v1/accounts/${route.params.name}/follow/`,
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
</script>

<style scoped>
.profile-container {
  max-width: 900px;
  margin: 0px auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.list-con {
  padding-top: 50px;
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: flex-start;
}

.profile-name {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.follow-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  background-color: #1da1f2;
  color: white;
  transition: all 0.3s ease;
}

button.following {
  background-color: #e0245e;
}

button:hover {
  opacity: 0.9;
}

button.following:hover {
  background-color: #c01e4e;
}
</style>