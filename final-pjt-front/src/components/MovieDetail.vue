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
          <p class="original-title">{{ movie.original_title }}</p>
          <div class="movie-meta">
            <span class="release-date">
              <i class="fas fa-calendar"></i>
              개봉일: {{ movie.release_date }}
            </span>
          </div>
          <button @click="showVideo(movie.youtube_url)" class="video-btn">
            <i class="fas fa-play"></i>
            예고편 보기
          </button>
        </div>
        <div class="movie-content">
          <h2>줄거리</h2>
          <p>{{ movie.overview }}</p>
        </div>
        <div class="calendar-add-section">
          <button @click="addToCalendarToday" class="calendar-add-btn">
            <i class="fas fa-calendar-plus"></i>
            오늘의 영화로 추가 
          </button>
        </div>
      </div>
    </div>

    <YoutubeModel ref="youtubeModal" />
  
    <div class="movie-comment-section">
      <div class="section-header">
        <h2>
          <i class="fas fa-comments"></i>
          댓글 ({{ movie.comments_count }})
        </h2>
      </div>

      <div class="comment-form">
        <div class="comment-input">
          <input 
            type="text" 
            v-model="newComment.text" 
            placeholder="영화에 대한 생각을 공유해보세요"
            maxlength="100"
          >
          <button @click="submitComment">
            <i class="fas fa-paper-plane"></i>
            작성
          </button>
        </div>
      </div>

      <div class="comments-list">
        <div v-if="!movie.comments || movie.comments.length === 0" class="no-comments">
          <i class="fas fa-comment-dots"></i>
          <p>첫 댓글을 작성해보세요!</p>
        </div>
        <template v-else>
          <div v-for="comment in paginatedComments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <div class="user-info">
                <div class="user-avatar">{{ comment.user.name.charAt(0).toUpperCase() }}</div>
                <span @click="goToCommentUserProfile(comment)" class="user-name">{{ comment.user.name }}</span>
              </div>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-text">{{ comment.content }}</p>
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
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import YoutubeModel from './YoutubeModel.vue';



const youtubeModal = ref(null);

const showVideo = (videoId) => {
  youtubeModal.value.openModal(videoId);
};
const route = useRoute()
const store = useCounterStore()
const movie = ref(null)
const newComment = ref({
  text: ''
})
const currentPage = ref(1)
const commentsPerPage = 10
const router=useRouter()

const goToCommentUserProfile = (comment) => {
  if (comment && comment.user) {
    router.push({
      name: 'mypage',
      params: { userName: comment.user.username }
    })
  }
}
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

const addToCalendarToday = async () => {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/movies/calendar/${store.currentUser.username}/select/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        tmdb_id: movie.value.tmdb_id
      }
    })

    if (response.status === 200) {
      alert('오늘의 영화로 등록되었습니다!')
    }
  } catch (error) {
    if (error.response?.status === 403) {
      alert('자신의 달력에만 영화를 선택할 수 있습니다.')
    } else if (error.response?.status === 400) {
      alert(error.response.data.error)
    } else {
      alert('영화 등록에 실패했습니다.')
    }
  }
}

onMounted(async () => {
  try {
    const movieId = route.params.id
    const response = await axios.get(`${store.API_URL}/community/movies/${movieId}/`)
    movie.value = response.data
    console.log(movie)
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
      url: `${store.API_URL}/community/movies/${route.params.id}/comments/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      data: {
        content: newComment.value.text
      }
    })

    // 댓글 목록 새로고침
    const response = await axios.get(`${store.API_URL}/community/movies/${route.params.id}/`)
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --font-primary: 'Noto Sans KR', sans-serif;
  --font-secondary: 'Poppins', sans-serif;
}

.movie-detail {
  min-height: 100vh;
  padding: 40px 20px;
  background: #1a1f2c;
  font-family: var(--font-primary);
}

.movie-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 40px;
  background: #242937;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.movie-poster {
  flex: 0 0 350px;
  position: relative;
}

.movie-poster img {
  width: 100%;
  height: 500px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.rating {
  position: absolute;
  top: 15px;
  left: 15px;
  background: rgba(220, 26, 40, 0.9);
  color: white;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-secondary);
}

.movie-info {
  flex: 1;
  color: #ffffff;
}

.movie-header h1 {
  font-size: 2.5rem;
  margin: 0 0 10px 0;
  color: #ffffff;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.original-title {
  color: #a0a0a0;
  font-size: 1.1rem;
  margin-bottom: 20px;
  letter-spacing: -0.01em;
}

.movie-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  color: #a0a0a0;
  font-family: var(--font-secondary);
}

.movie-content h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.movie-content p {
  line-height: 1.8;
  color: #a0a0a0;
  letter-spacing: -0.01em;
}
.video-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 15px;
}

.video-btn:hover {
  background: #b91521;
  transform: translateY(-2px);
}

.video-btn i {
  font-size: 0.9rem;
}

.calendar-add-btn {
  padding: 12px 24px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
}

.calendar-add-btn:hover {
  background: #b91521;
  transform: translateY(-2px);
}

.comment-form {
  background: #242937;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.comment-input {
  display: flex;
  gap: 12px;
  position: relative;
}

.comment-input input {
  flex: 1;
  padding: 12px 20px;
  background: #1a1f2c;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.95rem;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
  transition: all 0.2s ease;
}

.comment-input input:focus {
  outline: none;
  border-color: #dc1a28;
  box-shadow: 0 0 0 2px rgba(220, 26, 40, 0.2);
}

.comment-input input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  font-family: var(--font-primary);
}

.comment-input button {
  padding: 12px 24px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-primary);
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.comment-input button:hover {
  background: #b91521;
  transform: translateY(-2px);
}

.comment-input button i {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .comment-input {
    flex-direction: column;
  }

  .comment-input button {
    width: 100%;
    justify-content: center;
  }
}

.user-name {
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: -0.01em;
}

.user-name:hover {
  color: #dc1a28;
  transform: translateY(-1px);
}

.comment-date {
  color: #a0a0a0;
  font-size: 0.9rem;
  font-family: var(--font-secondary);
}

.comment-text {
  color: #ffffff;
  line-height: 1.6;
  letter-spacing: -0.01em;
}
/* 댓글 아이템 스타일 */
.comment-item {
  padding: 20px;
  background: #242937;
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

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #dc1a28;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-family: var(--font-secondary);
}

.user-name {
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
}

.user-name:hover {
  color: #dc1a28;
  transform: translateY(-1px);
}

.comment-date {
  color: #a0a0a0;
  font-size: 0.9rem;
  font-family: var(--font-secondary);
}

.comment-text {
  color: #ffffff;
  line-height: 1.6;
  font-family: var(--font-primary);
  letter-spacing: -0.01em;
}

/* 페이지네이션 스타일 */
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

  .movie-header h1 {
    font-size: 2rem;
  }
}
</style>