<template>
  <div class="follower-item">
    <div class="follower-avatar">
      <span>{{ follower.name.charAt(0).toUpperCase() }}</span>
    </div>
    <div class="follower-info">
      <h3 class="follower-name">{{ follower.name }}</h3>
      <p class="follower-email" v-if="follower.email">{{ follower.email }}</p>
    </div>
    <button @click="goToProfile" class="profile-btn">
      프로필
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  follower: {
    type: Object,
    required: true
  }
})

const goToProfile = () => {
  router.push({
    name: 'mypage',
    params: { userName: props.follower.username }
  })
}
</script>

<style scoped>
.follower-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #242937;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.follower-item:hover {
  transform: translateY(-2px);
}

.follower-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #dc1a28;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  margin-right: 1rem;
}

.follower-info {
  flex: 1;
}

.follower-name {
  margin: 0;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 500;
}

.follower-email {
  margin: 0.25rem 0 0;
  color: #9ca3af;
  font-size: 0.875rem;
}

.profile-btn {
  padding: 0.5rem 1rem;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.profile-btn:hover {
  background: #b91521;
}

@media (max-width: 640px) {
  .follower-item {
    padding: 0.75rem;
  }
  
  .follower-avatar {
    width: 40px;
    height: 40px;
  }
  
  .follower-name {
    font-size: 0.875rem;
  }
  
  .follower-email {
    font-size: 0.75rem;
  }
  
  .profile-btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>