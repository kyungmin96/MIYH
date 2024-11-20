<template>
  <div class="follower-item">
    <div class="follower-info">
      <p class="follower-name">{{ follower.username }}</p>
      <p class="follower-count">팔로워: {{ follower.followers_count }}</p>
    </div>
    <button @click="goToProfile" class="profile-btn">프로필 보기</button>
    <hr>
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
    params: { name: props.follower.name }
  })
}
</script>

<style scoped>
.follower-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.follower-info {
  margin-bottom: 1rem;
}

.follower-name {
  font-weight: bold;
  margin: 0.2rem 0;
}

.follower-count {
  color: #666;
  font-size: 0.9rem;
  margin: 0.2rem 0;
}

.profile-btn {
  padding: 8px 16px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-btn:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.profile-btn:active {
  transform: translateY(0);
}

hr {
  margin: 1rem 0;
  border: none;
  border-top: 1px solid #eee;
}
</style>