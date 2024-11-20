<template>
  <div class="article-list">
    <!-- 게시글 목록 -->
    <ArticleListItem
      v-for="article in paginatedArticles"
      :key="article.id"
      :article="article" 
    />

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1"
        @click="currentPage--"
        class="page-btn"
      >
        이전
      </button>
      
      <span class="page-numbers">
        <button 
          v-for="page in displayedPages" 
          :key="page"
          @click="currentPage = page"
          :class="['page-number', { active: currentPage === page }]"
        >
          {{ page }}
        </button>
      </span>

      <button 
        :disabled="currentPage === totalPages"
        @click="currentPage++"
        class="page-btn"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue';
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';

const articles = ref([])
const currentPage = ref(1)
const articlesPerPage = 5 // 페이지당 게시글 수

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
    const response = await axios.get('http://127.0.0.1:8000/community/posts/');
    articles.value = response.data;
    console.log('커뮤니티 완료:', response.data);
  } catch (error) {
    console.error('커뮤니티 실패:', error);
  }
});
</script>

<style scoped>
.article-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 0.5rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 4px;
}

.page-btn:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.page-number {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 4px;
}

.page-number.active {
  background-color: #4CAF50;
  color: white;
}

.page-btn:hover:not(:disabled),
.page-number:hover:not(.active) {
  background-color: #e0e0e0;
}
</style>