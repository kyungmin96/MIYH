<template>
  <div class="Article-container">
    <div class="Article-header">
      <h1>게시판</h1>
      <button @click="create" class="write-btn">글 작성</button>
    </div>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue';
import { useRouter } from 'vue-router';
import { onMounted,ref} from 'vue';
import axios from 'axios';
const router = useRouter()
const articles = ref(null)
const create = function () {
  router.push({ name: 'article-create'}) 
}
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/posts/');
    articles.value = response.data;
    console.log('커뮤니티 완료:', response.data);
  } catch (error) {
    console.error('커뮤니티 실패:', error);
  }
});
</script>

<style scoped>
.Article-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.Article-header {
  display: flex;
  justify-content: space-between; /* 양끝 정렬 */
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem 0;
  border-bottom: 2px solid #eee;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.write-btn {
  padding: 0.8rem 1.5rem;
  background-color: #4CAF50; /* 초록색 계열 */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.write-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .Article-container {
    padding: 1rem;
  }
  
  .Article-header {
    padding: 0.5rem 0;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .write-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}
</style>