<template>
  <div class="post-detail" v-if="article">
    <div class="post-header">
      <h1 class="post-title">{{ article?.title }}</h1>
      <div class="post-meta">
        <div class="meta-info">
          <span class="author">작성자: {{ article?.user.username }}</span>
          <span class="date">작성일: {{ article?.created_at}}</span>
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
        v-for="comment in article?.comments" 
        :key="comment.id" 
        class="comment-item"
      >
        <div class="comment-header">
          <span class="comment-author">{{ comment.user.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
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

const goBack =function(){
  router.push({ name: 'article'})
}
// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
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
      `http://127.0.0.1:8000/community/posts/${route.params.id}/comments/`,
      {
        content: newComment.value.content
      },
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )

    // 댓글 작성 후 게시글 정보 새로고침
    const response = await axios.get(
      `http://127.0.0.1:8000/community/posts/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    article.value = response.data
    
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
      `http://127.0.0.1:8000/community/posts/${postsId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    article.value = response.data
    console.log('게시글 상세 정보:', article)
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
        url: `http://127.0.0.1:8000/community/posts/${postsId}/like/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      
      // 게시글 정보를 새로 가져와서 업데이트
      const updatedArticle = await axios.get(
        `http://127.0.0.1:8000/community/posts/${postsId}/`,
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
      url: `http://127.0.0.1:8000/community/posts/${route.params.id}/`,
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
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-header {
  margin-bottom: 2rem;
}

.post-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}



.post-content {
  line-height: 1.6;
  color: #444;
  margin-bottom: 2rem;
}

.post-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}


.action-btn.edit {
  background: #4a90e2;
  color: white;
}

.action-btn.delete {
  background: #dc3545;
  color: white;
}

.action-btn.back {
  background: #6c757d;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.comments-section {
  margin-top: 3rem;
}

.comments-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  height: 100px;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-form button {
  padding: 0.5rem 1rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment-form button:hover {
  background: #357abd;
}

.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: #666;
  font-size: 0.9rem;
}

.comment-content {
  color: #444;
  line-height: 1.4;
}
.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
  font-size: 0.9rem;
}

.meta-info {
  display: flex;
  gap: 1rem;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  height: 36px;
  padding: 0 16px;
  border: 2px solid #ff4757;
  background: white;
  color: #ff4757;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-content {
  display: flex;
  align-items: center;
  gap: 6px;
}

.like-btn i {
  font-size: 1rem;
}

.like-count {
  font-size: 0.9rem;
  font-weight: 500;
}

.like-btn:hover {
  background: #fff5f6;
  transform: translateY(-1px);
}

.like-btn.liked {
  background: #ff4757;
  color: white;
  box-shadow: 0 2px 4px rgba(255, 71, 87, 0.2);
}

.like-btn.liked:hover {
  background: #ff6b81;
}

/* 클릭 효과 추가 */
.like-btn:active {
  transform: scale(0.95);
}

</style>