<template>
  <div class="write-item">
    <p class="title">{{ write.title }}</p>
    <p class="content">{{ write.content_preview }}</p>
    <button @click="goToDetail" class="detail-btn">상세 보기</button>
    <hr>
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
.write-item {
  padding: 1rem;
  margin-bottom: 1rem;
}

.title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.content {
  color: #666;
  margin-bottom: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.detail-btn {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 1rem 0;
}
</style>