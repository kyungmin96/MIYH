<template>
  <div class="following-item">
    <div class="following-info">
      <p class="following-name">{{ follower.username }}</p>
      <p class="following-email" v-if="follower.email">{{ follower.email }}</p>
    </div>
    <div class="following-actions">
      <button @click="goToProfile" class="profile-btn">프로필</button>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue';
const store =useCounterStore()
const route = useRoute()
const router = useRouter()
const profileData=ref()
// props 정의
const props = defineProps({
  follower: {
    type: Object,
    required: true
  }
})

// emit 정의
const emit = defineEmits(['unfollow'])

const goToProfile = () => {
  router.push({
    name: 'mypage',
    params: { name: props.follower.username }
  })
}

// route.params.name이 변경될 때마다 데이터를 다시 불러옴
watch(
  () => route.params.name,
  async (newUsername) => {
    if (newUsername) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/v1/accounts/profile/${newUsername}/`,
          {
            headers: {
              Authorization: `Token ${store.token}`
            }
          }
        )
        // 새로운 프로필 데이터로 업데이트
        profileData.value = response.data
      } catch (error) {
        console.error('프로필 로드 실패:', error)
        if (error.response?.status === 404) {
          alert('존재하지 않는 사용자입니다.')
          router.push('/')
        }
      }
    }
  },
  { immediate: true }
)

const handleUnfollow = () => {
  emit('unfollow', props.follower.username)
}
</script>

<style scoped>
.following-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
}

.following-info {
  flex-grow: 1;
}

.following-name {
  font-weight: bold;
  margin: 0;
}

.following-email {
  color: #666;
  margin: 4px 0 0 0;
  font-size: 0.9em;
}

.following-actions {
  display: flex;
  gap: 8px;
}

.profile-btn, .unfollow-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.profile-btn {
  background-color: #4a90e2;
  color: white;
}

.unfollow-btn {
  background-color: #dc3545;
  color: white;
}

.profile-btn:hover {
  background-color: #357abd;
}

.unfollow-btn:hover {
  background-color: #c82333;
}
</style>