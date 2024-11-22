<template>
  <div class="follower-list">
    <h2 class="follower-title">
      <i class="fas fa-user-friends"></i>
      팔로잉 목록
    </h2>
    <div class="follower-content">
      <div v-if="profileData?.followings_list
.length === 0" class="no-follower">
        <div class="empty-state">
          <div class="empty-content">
          <i class="fas fa-users"></i>
          <p>아직 팔로잉가 없습니다</p>
        </div>
      </div>
      </div>
      <div v-else class="follower-grid">
        <FollowingListItem 
          v-for="follower in profileData?.followings_list
" 
          :key="follower.id"
          :follower="follower"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import FollowingListItem from './FollowingListItem.vue';

const route = useRoute()
const store = useCounterStore()
const props = defineProps({
  profileData: {
    type: Object,
    required: true
  }
})

// route.params.name이 변경될 때마다 데이터를 다시 불러옴
watch(
  () => route.params.userName,
  (newName) => {
    if (newName && store.token) {
    }
  }
)
</script>

<style scoped>
.follower-list {
  width: 100%;
  max-width: 400px;
  max-width: 800px;
  height: 600px;
  margin: 0 auto;
  background: #1a1f2e;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.follower-title {
  
  padding: 1.5rem;
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
  background: #242937;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.follower-title i {
  color: #dc1a28;
}

.follower-content {
  height: 100%;
  min-height: 200px;
  padding: 1rem;
}

.empty-state {
  height: 100%;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.empty-content i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.empty-content p {
  margin: 0;
  font-size: 0.95rem;
}
.follower-grid {
  display: grid;
  gap: 1rem;
}

.follower-content::-webkit-scrollbar {
  width: 5px;
}

.follower-content::-webkit-scrollbar-track {
  background: #1a1f2e;
}

.follower-content::-webkit-scrollbar-thumb {
  background: #2a2f3e;
  border-radius: 20px;
}

.follower-content::-webkit-scrollbar-thumb:hover {
  background: #3a3f4e;
}
</style>