<template>
  <div class="follower-list">
    <h1>팔로워 목록</h1>
    <div class="follower-content">
      <FollowerLisetitem
        v-for="fowller in store.fowllers"
        :key="fowller.name"
        :fowller="fowller" 
      />
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import FollowerLisetitem from './FollowerLisetitem.vue';
const store = useCounterStore()
</script>

<style scoped>
.follower-list {
  width: 33%;
  height: 40vh; /* 이전 컴포넌트와 동일한 높이 */
  border: 1px solid #ccc;
  padding: 15px;
}

.follower-content {
  border: 1px solid #ccc;
  border-radius: 8px;
  height: calc(80% - 50px); /* h1 높이를 고려하여 조정 */
  overflow-y: auto; /* 세로 스크롤만 표시 */
  overflow-x: hidden; /* 가로 스크롤 숨김 */
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