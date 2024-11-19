<template>
  <div class="profile-container">
    <div class="profile-name">
      <h1>이름 님의 프로필</h1>
      <div class="follow-section">
        <span>팔로워 수: {{ followerCount }}</span>
        <button 
          @click="toggleFollow" 
          :class="{ 'following': isFollowing }"
        >
          {{ isFollowing ? '팔로우 취소' : '팔로우' }}
        </button>
      </div>
    </div>
    <div class="list-con">
      <WriteList />
      <FollowerList />
      <TodayMovie />
    </div>
  </div>
</template>


<script setup>
import WriteList from '@/components/WriteList.vue';
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter';
import FollowerList from '@/components/FollowerList.vue';
import TodayMovie from '@/components/TodayMovie.vue';

const isFollowing = ref(false)
const followerCount = ref(0)
const store = useCounterStore()
const toggleFollow = () => {
  isFollowing.value = !isFollowing.value
  // 팔로워 수 업데이트
  followerCount.value += isFollowing.value ? 1 : -1
}
</script>

<style scoped>
.profile-container {
  max-width: 900px;
  margin: 0px auto;
  padding: 20px;
}
.list-con {
  padding-top: 50px;
  display: flex;
  gap: 20px; /* 컴포넌트 사이의 간격 */
  justify-content: center; /* 가운데 정렬 */
  align-items: flex-start; /* 위쪽 정렬 */
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
.list-con{
  display: flex;
}
</style>