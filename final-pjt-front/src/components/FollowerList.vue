<!-- FollowerList.vue -->
<template>
  <div class="follower-list">
    <h1>팔로워 목록</h1>
    <div class="follower-content">
      <div v-if="loading" class="loading">
        Loading...
      </div>
      <div v-else-if="profileData?.followers_list === 0" class="no-followers">
        팔로워가 없습니다.
      </div>
      <div v-else class="followers">
        <FollowerLisetitem
        v-for="follower in profileData?.followers_list"
          :key="follower.id"
          :follower="follower"
          @unfollow="unfollowUser"
          />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import FollowerLisetitem from '@/components/FollowerLisetitem.vue';

const props = defineProps({
  profileData: {
    type: Object,
    required: true
  }
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