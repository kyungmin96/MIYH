<template>
  <div class="movie-detail" v-if="movie">
    <div class="movie-detail-container">
      <div class="movie-poster">
        <img :src="movie.poster_url" :alt="movie.title">
        <div class="rating">
          <i class="fas fa-fire"></i> {{ movie.popularity }}
        </div>
      </div>
      <div class="movie-info">
        <div class="movie-header">
          <h1>{{ movie.title }}</h1>
          <p>{{ movie.original_title }}</p>
          <div class="movie-meta">
            <span class="release-date">개봉일: {{ movie.release_date }}</span>
          </div>
        </div>
        <div class="movie-content">
          <h2>줄거리</h2>
          <p>{{ movie.overview }}</p>
        </div>
      </div>
    </div>

    <div class="movie-comment-section">
      <h2>댓글 ({{ movie.comments_count }})</h2>
      <div class="comment-form">
        <div class="comment-input">
          <input 
            type="text" 
            v-model="newComment.text" 
            placeholder="댓글을 입력하세요"
            maxlength="100"
          >
          <button @click="submitComment">작성</button>
        </div>
      </div>

      <div class="comments-list">
    <div v-if="!movie.comments || movie.comments.length === 0" class="no-comments">
      첫 댓글을 작성해보세요!
    </div>
    <template v-else>
      <!-- 현재 페이지의 댓글만 표시 -->
      <div v-for="comment in paginatedComments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="user-name">{{ comment.user.username }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-text">{{ comment.content }}</p>
      </div>

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
    </template>
  </div>

    <div class="calendar-add-section">
      <button @click="addToCalendarToday" class="calendar-add-btn">
        오늘 날짜로 달력에 추가
      </button>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const route = useRoute()
const store = useCounterStore()
const movie = ref(null)
const newComment = ref({
  text: ''
})
const currentPage = ref(1)
const commentsPerPage = 10

// 페이지네이션된 댓글 목록
const paginatedComments = computed(() => {
  if (!movie.value?.comments) return []
  const start = (currentPage.value - 1) * commentsPerPage
  const end = start + commentsPerPage
  return movie.value.comments.slice(start, end)
})

// 전체 페이지 수
const totalPages = computed(() => {
  if (!movie.value?.comments) return 0
  return Math.ceil(movie.value.comments.length / commentsPerPage)
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

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

// 오늘 날짜 가져오기
const getCurrentDate = () => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const addToCalendarToday = () => {
  const today = getCurrentDate()
  const newEvent = {
    start: today,
    allDay: true,
    display: 'background',
    extendedProps: {
      imageUrl: movie.value.poster_url,
      movieId: movie.value.id,
      title: movie.value.title
    }
  }

  try {
    store.addOrUpdateEvent(newEvent)
    alert('오늘의 영화로 등록되었습니다!')
  } catch (error) {
    alert('영화 등록에 실패했습니다.')
  }
}

onMounted(async () => {
  try {
    const movieId = route.params.id
    const response = await axios.get(`http://127.0.0.1:8000/community/movies/${movieId}/`)
    movie.value = response.data
    console.log('영화 상세 정보:', movie.value)
  } catch (error) {
    console.error('영화 정보 로드 실패:', error)
  }
})

const submitComment = async () => {
  if (!newComment.value.text) {
    alert('댓글을 입력해주세요')
    return
  }

  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/community/movies/${route.params.id}/comments/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        content: newComment.value.text
      }
    })

    // 댓글 목록 새로고침
    const response = await axios.get(`http://127.0.0.1:8000/community/movies/${route.params.id}/`)
    movie.value = response.data
    
    // 입력 폼 초기화
    newComment.value.text = ''
    alert('댓글이 등록되었습니다.')
  } catch (error) {
    console.error('댓글 등록 실패:', error)
    alert('댓글 등록에 실패했습니다.')
  }
}
</script>


<style scoped>
.movie-detail {
  min-height: 100vh;
  background-color: #1a1a1a;
  padding: 2rem;
}

.movie-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
  background: #2d2d2d;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.movie-poster {
  flex: 0 0 300px;
  position: relative;
}

.movie-poster img {
  width: 100%;
  height: 450px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.new-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff4757;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: bold;
}

.rating {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0,0,0,0.7);
  color: #ffd700;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 1.1rem;
}

.movie-info {
  flex: 1;
  color: #fff;
}

.movie-header h1 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
  color: #fff;
}

.movie-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  color: #ccc;
}

.movie-meta span {
  padding-right: 1rem;
  border-right: 1px solid #555;
}

.movie-meta span:last-child {
  border-right: none;
}

.movie-content h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #fff;
}

.movie-content p {
  line-height: 1.6;
  color: #ccc;
  margin-bottom: 2rem;
}


.movie-comment-section {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: #2d2d2d;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.movie-comment-section h2 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.comment-form {
  background: #383838;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.rating-input {
  margin-bottom: 1rem;
  color: #fff;
}

.rating-input select {
  margin-left: 1rem;
  padding: 0.5rem;
  background: #2d2d2d;
  color: #ffd700;
  border: 1px solid #555;
  border-radius: 4px;
}

.comment-input {
  display: flex;
  gap: 1rem;
}

.comment-input input {
  flex: 1;
  padding: 0.8rem;
  background: #2d2d2d;
  border: 1px solid #555;
  border-radius: 4px;
  color: #fff;
}

.comment-input button {
  padding: 0.8rem 1.5rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.comment-input button:hover {
  background: #357abd;
  transform: translateY(-2px);
}

.comments-list {
  margin-top: 2rem;
}

.no-comments {
  text-align: center;
  color: #888;
  padding: 2rem;
}

.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #383838;
  color: #fff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.user-name {
  color: #4a90e2;
  font-weight: bold;
}

.comment-text {
  color: #ccc;
  line-height: 1.4;
}

.comment-date {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #888;
}

@media (max-width: 768px) {
  .movie-detail-container {
    flex-direction: column;
    padding: 1rem;
  }

  .movie-poster {
    flex: none;
    width: 100%;
  }

  .movie-poster img {
    height: 300px;
  }

  .comment-input {
    flex-direction: column;
  }

  .comment-input button {
    width: 100%;
  }
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
  background-color: #4a90e2;
  color: white;
}

.page-btn:hover:not(:disabled),
.page-number:hover:not(.active) {
  background-color: #e0e0e0;
}
.calendar-add-section {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.calendar-add-btn {
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.calendar-add-btn.secondary {
  background-color: #2ecc71;
}

.calendar-add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.calendar-add-btn.secondary:hover {
  background-color: #27ae60;
}
</style>