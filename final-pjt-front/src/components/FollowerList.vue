<!-- FollowerList.vue -->
<template>
  <div class="follower-list">
    <h1>팔로잉 목록</h1>
    <div class="follower-content">
      <div v-if="loading" class="loading">
        Loading...
      </div>
      <div v-else-if="followers.length === 0" class="no-followers">
        팔로워가 없습니다.
      </div>
      <div v-else class="followers">
        <FollowerItem
          v-for="follower in followers"
          :key="follower.id"
          :follower="follower"
          @unfollow="unfollowUser"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
// import FollowerItem from './FollowerItem.vue'  // 팔로워 아이템 컴포넌트 import

const route = useRoute()
const store = useCounterStore()
const loading = ref(true)
const followers = ref([])

const fetchFollowers = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/accounts/profile/${route.params.name}/followers/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    followers.value = response.data
    console.log('팔로워 목록:', response.data)
  } catch (error) {
    console.error('팔로워 목록 로드 실패:', error)
  } finally {
    loading.value = false
  }
}

const unfollowUser = async (username) => {
  try {
    await axios({
      method: 'DELETE',
      url: `http://127.0.0.1:8000/api/v1/accounts/profile/${username}/followers/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    await fetchFollowers()
  } catch (error) {
    console.error('언팔로우 실패:', error)
  }
}

onMounted(() => {
  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }
  fetchFollowers()
})
</script>