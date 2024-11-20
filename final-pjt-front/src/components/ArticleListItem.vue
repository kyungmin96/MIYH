<template>
  <div class="article-item">
    <div class="article-header">
      <div class="header-left">
        <span class="category">{{ article.category }}</span>
        <span class="article-author">
          <i class="fas fa-user"></i> {{ article.user.username }}
        </span>
      </div>
      <div class="article-stats">
        <span class="stat-item">
          <i class="fas fa-comment"></i> {{ article.comments_count }}
        </span>
        <span class="stat-item">
          <i class="fas fa-heart"></i> {{ article.like_users_count }}
        </span>
      </div>
    </div>

    <h2 class="article-title">{{ article.title }}</h2>
    <p class="article-content">{{ article.content }}</p>
    
    <div class="article-footer">
      <button @click="goToDetail" class="detail-btn">
        상세 보기
        <i class="fas fa-arrow-right"></i>
      </button>
    </div>
  </div>
</template>


<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  article: Object
})

const goToDetail = () => {
  router.push({
    name: 'article-detail',
    params: { id: props.article.id }
  })
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.article-author {
  color: #6c757d;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}
.article-author i {
  font-size: 0.8rem;
}

.article-item {
  background: #fff;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.article-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.category {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 500;
}

.article-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  color: #6c757d;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.article-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.8rem;
}

.article-content {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.article-footer {
  display: flex;
  justify-content: flex-end;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.detail-btn {
  padding: 0.6rem 1.2rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.detail-btn i {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.detail-btn:hover i {
  transform: translateX(3px);
}
</style>