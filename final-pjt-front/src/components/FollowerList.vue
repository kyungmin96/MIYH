<template>
  <div class="follower-list">
    <h2 class="follower-title">
      <i class="fas fa-users"></i>
      팔로워 목록
    </h2>
    <div class="follower-content">
      <div v-if="profileData?.followers_list.length === 0" class="no-follower">
        <div class="empty-state">
          <div class="empty-content">
          <i class="fas fa-users"></i>
          <p>아직 팔로워가 없습니다</p>
        </div>
      </div>
      </div>
      <div v-else class="follower-grid">
        <FollowerListItem
          v-for="follower in profileData?.followers_list"
          :key="follower.id"
          :follower="follower"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import FollowerListItem from '@/components/FollowerLisetitem.vue';


const props = defineProps({
  profileData: {
    type: Object,
    required: true
  }
})

</script>


<style scoped>

.follower-list {
  width: 100%;
  max-width: 400px;
  max-width: 800px;
  height: 600px;
  margin: 0 auto;
  background: #1a1f2e;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.follower-title {
  padding: 1.5rem;
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
  background: #242937;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
</style>