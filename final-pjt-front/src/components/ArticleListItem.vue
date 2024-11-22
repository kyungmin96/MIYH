<template>
  <div class="article-item">
    <div class="article-header">
      <div class="header-left">
        <div class="author-info">
          <div class="author-avatar">
            {{ article.user.username.charAt(0).toUpperCase() }}
          </div>
          <span class="article-author" @click="goToUserProfile" role="button">
            {{ article.user.name }}
          </span>
        </div>
        <span class="category">{{ article.category }}</span>
      </div>
      <div class="article-stats">
        <span class="stat-item">
          <i class="fas fa-comment"></i>
          {{ article.comments_count }}
        </span>
        <span class="stat-item">
          <i class="fas fa-heart"></i>
          {{ article.like_users_count }}
        </span>
      </div>
    </div>

    <div class="article-content">
      <h2 class="article-title">{{ article.title }}</h2>
      <p class="article-text">{{ article.content }}</p>
    </div>
    
    <div class="article-footer">
      <button @click="goToDetail" class="detail-btn">
        <span>글 보기</span>
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
const goToUserProfile = () => {
  router.push({
    name: 'mypage',
    params: { userName: props.article.user.username }
  })
}
</script>

<style scoped>
.article-item {
  background: linear-gradient(145deg, #1f2937, #1a1a2e);
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.article-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e50914, #b2070f);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  box-shadow: 0 2px 10px rgba(229, 9, 20, 0.2);
}

.article-author {
  color: #ffffff;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.article-author:hover {
  color: #e50914;
  text-decoration: underline;
}
.category {
  background: rgba(229, 9, 20, 0.1);
  color: #e50914;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  border: 1px solid rgba(229, 9, 20, 0.2);
}

.article-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  color: #b3b3b3;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-item i {
  color: #e50914;
}

.article-content {
  padding: 10px 0;
}

.article-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 12px;
}

.article-text {
  color: #b3b3b3;
  line-height: 1.6;
  margin-bottom: 20px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.article-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-btn {
  padding: 10px 20px;
  background: linear-gradient(145deg, #e50914, #b2070f);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(229, 9, 20, 0.2);
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(229, 9, 20, 0.3);
  background: linear-gradient(145deg, #f40612, #e50914);
}

.detail-btn i {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.detail-btn:hover i {
  transform: translateX(3px);
}

@media (max-width: 768px) {
  .article-item {
    padding: 20px;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .article-title {
    font-size: 1.2rem;
  }

  .detail-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>