<template>
  <div class="article-container">
    <div class="article-header">
      <div class="header-content">
        <div class="title-section">
          <i class="fas fa-film"></i>
          <h1>영화 토크</h1>
          <span class="subtitle">다양한 영화 이야기를 나눠보세요</span>
        </div>
        <button @click="create" class="create-btn">
          <i class="fas fa-pen"></i>
          <span>글 작성</span>
        </button>
      </div>
    </div>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue';
import { useRouter } from 'vue-router';

const router = useRouter()


const create = function () {
  router.push({ name: 'article-create'}) 
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.article-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
  position: relative;
  font-family: var(--font-primary);
}

.article-header {
  margin-bottom: 30px;
  padding: 30px 35px;
  background: #1a1f2c;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.title-section i {
  font-size: 32px;
  color: #dc1a28;
  margin-bottom: 5px;
}

h1 {
  font-size: 1.8rem;
  color: #ffffff;
  margin: 0;
  font-weight: 700;
  letter-spacing: -0.03em;
  font-family: var(--font-primary);
}

.subtitle {
  color: #a0a0a0;
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
}

.create-btn i {
  font-size: 0.9rem;
}

.create-btn:hover {
  background: #b91521;
  transform: translateY(-2px);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .article-container {
    margin: 20px auto;
    padding: 0 15px;
  }

  .article-header {
    padding: 25px;
  }

  .title-section {
    gap: 5px;
  }

  .title-section i {
    font-size: 28px;
  }

  h1 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.85rem;
  }

  .create-btn {
    padding: 10px 20px;
    font-size: 0.85rem;
  }
}
</style>