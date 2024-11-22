<template>
  <div class="post-item">
    <div class="post-content">
      <h3 class="post-title">{{ write.title }}</h3>
      <p class="post-preview">{{ write.content_preview }}</p>
    </div>
    
    <div class="post-footer">
      <button @click="goToDetail" class="view-btn">
        <span>상세 보기</span>
        <i class="fas fa-arrow-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  write: Object
})

const goToDetail = () => {
  router.push({
    name: 'article-detail',
    params: { id: props.write.id }
  })
}
</script>

<style scoped>
.post-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.post-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.post-title {
  color: #ffffff;
  font-size: 1.1rem;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.post-preview {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.view-btn {
  background: #dc1a1a;
  color: #ffffff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: #c41717;
}

.view-btn i {
  font-size: 0.8rem;
}
</style>