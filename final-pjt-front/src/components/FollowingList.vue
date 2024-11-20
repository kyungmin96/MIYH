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
        <div v-for="follower in followers" :key="follower.id" class="follower-item">
          <FollowingListItem 
            :follower="follower"
            @unfollow="unfollowUser"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import FollowingListItem from './FollowingListItem.vue';

const route = useRoute()
const store = useCounterStore()
const loading = ref(true)
const followers = ref([])

// 팔로워 목록 가져오기
const fetchFollowers = async () => {
  try {
    loading.value = true
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

// 언팔로우 기능
const unfollowUser = async (username) => {
  try {
    await axios({
      method: 'DELETE',
      url: `http://127.0.0.1:8000/api/v1/accounts/profile/${username}/followers/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    // 목록 새로고침
    await fetchFollowers()
  } catch (error) {
    console.error('언팔로우 실패:', error)
  }
}

// route.params.name이 변경될 때마다 데이터를 다시 불러옴
watch(
  () => route.params.name,
  (newName) => {
    if (newName && store.token) {
      fetchFollowers()
    }
  }
)

onMounted(() => {
  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }
  fetchFollowers()
})
</script>

<style scoped>
.follower-list {
  width: 33%;
  height: 40vh;
  border: 1px solid #ccc;
  padding: 15px;
}

.follower-content {
  border: 1px solid #ccc;
  border-radius: 8px;
  height: calc(80% - 50px);
  overflow-y: auto;
  overflow-x: hidden;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.no-followers {
  text-align: center;
  padding: 20px;
  color: #666;
}

.follower-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.follower-name {
  font-weight: bold;
}

.unfollow-btn {
  padding: 5px 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.unfollow-btn:hover {
  background-color: #c82333;
}

/* 스크롤바 스타일링 */
.follower-content::-webkit-scrollbar {
  width: 8px;
}

.follower-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.follower-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.follower-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>