<template>
  <div class="article-list">
    <div class="articles-container">
      <ArticleListItem
        v-for="article in paginatedArticles"
        :key="article.id"
        :article="article" 
      />
      
      <div v-if="!paginatedArticles.length" class="no-articles">
        <i class="fas fa-film"></i>
        <p>아직 작성된 리뷰가 없습니다</p>
        <span>첫 번째 영화 리뷰를 작성해보세요!</span>
      </div>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1"
        @click="currentPage--"
        class="page-btn"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in displayedPages" 
          :key="page"
          @click="currentPage = page"
          :class="['page-number', { active: currentPage === page }]"
        >
          {{ page }}
        </button>
      </div>

      <button 
        :disabled="currentPage === totalPages"
        @click="currentPage++"
        class="page-btn"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue';
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
const articles = ref([])
const currentPage = ref(1)
const articlesPerPage = 5 // 페이지당 게시글 수
const store = useCounterStore()
// 현재 페이지의 게시글만 표시
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage
  const end = start + articlesPerPage
  return articles.value.slice(start, end)
})

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(articles.value.length / articlesPerPage)
})

// 표시할 페이지 번호
const displayedPages = computed(() => {
  const pages = []
  const maxPages = 5 // 한 번에 표시할 최대 페이지 수

  let start = Math.max(1, currentPage.value - Math.floor(maxPages / 2))
  let end = Math.min(totalPages.value, start + maxPages - 1)

  if (end - start + 1 < maxPages) {
    start = Math.max(1, end - maxPages + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

onMounted(async () => {
  try {
    const response = await axios.get(`${store.API_URL}/community/posts/`);
    articles.value = response.data;
  } catch (error) {
    console.error('커뮤니티 실패:', error);
  }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.article-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  font-family: var(--font-primary);
}

.articles-container {
  background: #1a1f2c;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  min-height: 400px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.no-articles {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  text-align: center;
  color: #a0a0a0;
}

.no-articles i {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #dc1a28;
}

.no-articles p {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #ffffff;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.no-articles span {
  color: #a0a0a0;
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2.5rem;
  gap: 0.8rem;
  font-family: var(--font-secondary);
}

.page-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: #242937;
  color: #ffffff;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: 600;
}

.page-btn:disabled {
  background: #1a1f2c;
  color: #4a5568;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.8rem;
}

.page-number {
  width: 40px;
  height: 40px;
  border: none;
  background: #242937;
  color: #ffffff;
  cursor: pointer;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-family: var(--font-secondary);
}

.page-number.active {
  background: #dc1a28;
  color: white;
  border: none;
}

.page-btn:hover:not(:disabled),
.page-number:hover:not(.active) {
  transform: translateY(-2px);
  background: #2d3340;
}

@media (max-width: 768px) {
  .article-list {
    padding: 0 15px;
  }

  .articles-container {
    padding: 20px;
  }

  .pagination {
    gap: 0.6rem;
  }

  .page-btn,
  .page-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }

  .no-articles p {
    font-size: 1.1rem;
  }

  .no-articles span {
    font-size: 0.85rem;
  }
}
</style>