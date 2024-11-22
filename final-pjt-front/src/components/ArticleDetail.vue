<template>
  <div class="post-detail" v-if="article">
    <div class="post-header">
      <h1 class="post-title">{{ article?.title }}</h1>
      <div class="post-meta">
        <div class="meta-info">
          <span>작성자 : <span class="author" @click="goToUserProfile" > {{ article?.user.name }}</span></span>
          <span class="date">작성일 : {{ article?.created_at}}</span>
        </div>
        <button 
          @click.prevent="handleLike" 
          class="like-btn"
          :class="{ 
            'liked': article?.is_liked,
            'disabled': isAuthor 
          }"
        >
          <div class="like-content">
            <i class="fas fa-heart"></i>
            <span class="like-count">{{ article?.like_users_count }}</span>
          </div>
        </button>
      </div>
    </div>

    <div class="post-content">
      <p>{{ article?.content }}</p>
    </div>

    <div class="post-actions">
      <button 
        v-if="isAuthor"
        @click="handleEdit"
        class="action-btn edit"
      >
        수정
      </button>
      <button 
        v-if="isAuthor"
        @click="handleDelete"
        class="action-btn delete"
      >
        삭제
      </button>
      <button 
        @click="goBack" 
        class="action-btn back"
      >
        목록으로
      </button>
    </div>

    <div class="comments-section">
    <h2>댓글</h2>
    <div class="comment-form">
      <textarea 
        v-model="newComment.content"
        placeholder="댓글을 입력하세요"
      ></textarea>
      <button @click="submitComment">댓글 작성</button>
    </div>
    
    <div class="comments-list">
      <div 
        v-for="comment in paginatedComments" 
        :key="comment.id" 
        class="comment-item"
      >
        <div class="comment-header">
          <span @click="goToCommentUserProfile(comment)" class="comment-author">{{ comment.user.name }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>

    <!-- 페이지네이션 -->
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
  </div>
</template>

<script setup>
import { ref, onMounted,watchEffect,computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()
const article = ref(null)
const newComment = ref({
  content: ''
})
const currentPage = ref(1)
const commentsPerPage = 10

const paginatedComments = computed(() => {
  const start = (currentPage.value - 1) * commentsPerPage
  const end = start + commentsPerPage
  return article.value?.comments.slice(start, end) || []
})

const totalPages = computed(() => {
  return Math.ceil((article.value?.comments.length || 0) / commentsPerPage)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPages = 5
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

const goBack =function(){
  router.push({ name: 'article'})
}
// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}
const goToUserProfile = () => {
  if (article.value && article.value.user) {
    router.push({
      name: 'mypage',
      params: { userName: article.value.user.username }
    })
  }
}

const goToCommentUserProfile = (comment) => {
  if (comment && comment.user) {
    router.push({
      name: 'mypage',
      params: { userName: comment.user.username }
    })
  }
}

// 댓글 작성 함수
const submitComment = async () => {
  if (!newComment.value.content.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  try {
    await axios.post(
      `${store.API_URL}/community/posts/${route.params.id}/comments/`,
      {
        content: newComment.value.content
      },
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
        
      }
    ).then(
    )
    // 댓글 작성 후 게시글 정보 새로고침

    const response = await axios.get(
      `${store.API_URL}/community/posts/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    article.value = response.data
    console.log(response)
    // 입력 폼 초기화
    newComment.value.content = ''
    alert('댓글이 등록되었습니다.')
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다.')
  }
}

// 게시글 로드
onMounted(async () => {
  try {
    const postsId = route.params.id
    const response = await axios.get(
      `${store.API_URL}/community/posts/${postsId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    article.value = response.data
      console.log(article)
  } catch (error) {
    console.error('게시글 정보 로드 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push('/login')
    }
  }
})
// 좋아요 핸들러 함수 추가
const handleLike = async () => {
  // 작성자가 자신의 글에 좋아요를 누르려고 할 때
  if (isAuthor.value) {
    alert('자신의 글에는 좋아요를 할 수 없습니다.')
    return
  }
  // 기존 좋아요 로직 실행
  await likes()
}

const likes = async function () {
    const postsId = route.params.id
    try {
      const response = await axios({
        method: 'post',
        url: `${store.API_URL}/community/posts/${postsId}/like/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      
      // 게시글 정보를 새로 가져와서 업데이트
      const updatedArticle = await axios.get(
        `${store.API_URL}/community/posts/${postsId}/`,
        {
          headers: {
            Authorization: `Token ${store.token}`
          }
        }
      )
      
      // article ref 업데이트
      article.value = updatedArticle.data
      
    } catch (error) {
      console.error('좋아요 처리 실패:', error)
      if (error.response?.status === 401) {
        alert('로그인이 필요한 서비스입니다.')
        router.push('/login')
      }
    }
}

// 반응성 감시
watchEffect(() => {
  if (article.value) {
  }
})
const isAuthor_like = computed(() => {
  return article.value?.user.id !== store.currentUser.pk
})

const isAuthor = computed(() => {
  return article.value?.user.id === store.currentUser.pk
})

// 수정 버튼 클릭 핸들러
const handleEdit = () => {
  router.push({
    name: 'article-edit',
    params: { id: route.params.id }
  })
}

const handleDelete = async () => {
  try {
    if (!confirm('정말 이 게시글을 삭제하시겠습니까?')) {
      return
    }

    const response = await axios({
      method: 'delete',
      url: `${store.API_URL}/community/posts/${route.params.id}/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })

    if (response.status === 204) {
      alert('게시글이 삭제되었습니다.')
      router.push({ name: 'article' })
    }
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push('/login')
    } else if (error.response?.status === 403) {
      alert('삭제 권한이 없습니다.')
    } else {
      alert('게시글 삭제에 실패했습니다.')
    }
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.like-count {
  padding-left: 5px;
  font-family: var(--font-secondary);
}

.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: #1a1f2c;
  border-radius: 12px;
  color: #fff;
  font-family: var(--font-primary);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.post-header {
  margin-bottom: 2rem;
}

.post-title {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 1rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #8b95a9;
  font-size: 0.9rem;
  letter-spacing: -0.01em;
}

.meta-info {
  display: flex;
  gap: 1rem;
}

.post-content {
  line-height: 1.6;
  color: #d1d5db;
  margin-bottom: 2rem;
  letter-spacing: -0.01em;
}

.post-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.author {
  color: #ffffff;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: -0.01em;
}

.author:hover {
  color: #dc1a28;
  transform: translateY(-1px);
  text-shadow: 0 2px 4px rgba(220, 26, 40, 0.2);
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
}

.action-btn.edit {
  background-color: #6c757d;
  color: white;
  padding: 8px 16px;
}

.action-btn.delete {
  background-color: #dc3545;
  color: white;
  padding: 8px 16px;
}

.action-btn.back {
  background: #2d3446;
  color: white;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  height: 36px;
  padding: 0 16px;
  border: 2px solid #dc1a28;
  background: transparent;
  color: #dc1a28;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.like-btn.liked {
  background: #dc1a28;
  color: white;
}


.comments-section {
  margin-top: 3rem;
  background: #242937;
  border-radius: 8px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.comments-section h2 {
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  font-family: var(--font-primary);
}

/* 댓글 입력 폼 */
.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  min-height: 100px;
  background: #1a1f2c;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.95rem;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
  transition: all 0.2s ease;
  margin-bottom: 15px;
  resize: vertical;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #dc1a28;
  box-shadow: 0 0 0 2px rgba(220, 26, 40, 0.2);
}

.comment-form textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.comment-form button {
  padding: 12px 24px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
}

.comment-form button:hover {
  background: #b91521;
  transform: translateY(-2px);
}

/* 댓글 목록 */
.comment-item {
  padding: 20px;
  background: #1a1f2c;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-author {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: -0.01em;
  font-family: var(--font-primary);
}

.comment-author:hover {
  color: #dc1a28;
  transform: translateY(-1px);
}

.comment-date {
  color: #8b95a9;
  font-size: 0.9rem;
  font-family: var(--font-secondary);
}

.comment-content {
  color: #d1d5db;
  line-height: 1.6;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
  font-family: var(--font-primary);
}

/* 댓글이 없을 때 */
.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #8b95a9;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
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
  .pagination {
    gap: 0.6rem;
  }

  .page-btn,
  .page-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
}
</style>