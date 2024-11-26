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
import { watch } from 'vue';
import { useRouter,useRoute  } from 'vue-router'

const route =useRoute()
const router = useRouter()

const props = defineProps({
  follower: {
    type: Object,
    required: true
  }
})

const goToProfile = async () => {
  const userName = props.follower.username
  if (route.name === 'mypage' && route.params.userName === userName) {
    // 현재 페이지를 새로고침
    await router.replace({ name: 'mypage', params: { userName } })
  } else {
    // 새 페이지로 이동
    await router.push({ name: 'mypage', params: { userName } })
  }
}

</script>

<style scoped>
.follower-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #242937;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-bottom: 10px;
}

.follower-item:hover {
  transform: translateY(-2px);
  background: #2a2f3e;
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
  margin-right: 15px;
  font-size: 1.2rem;
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
  margin: 4px 0 0;
  color: #9ca3af;
  font-size: 0.875rem;
}

.profile-btn {
  padding: 8px 16px;
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
    padding: 12px;
  }
  
  .follower-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .follower-name {
    font-size: 0.875rem;
  }
  
  .follower-email {
    font-size: 0.75rem;
  }
  
  .profile-btn {
    padding: 6px 12px;
    font-size: 0.75rem;
  }
}
</style>