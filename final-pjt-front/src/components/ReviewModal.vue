<template>
  <div v-if="show" class="modal-backdrop">
    <div class="modal-content">
      <div class="modal-header">
        <h3>오늘, 이 영화와 함께</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="movie-info">
        <img :src="moviePoster" :alt="movieTitle" class="movie-poster">
        <h4 class="movie-title">{{ movieTitle }}</h4>
      </div>

      <div class="modal-body">
        <div v-if="!isEditing && movieComment" class="review-display">
          <p class="review-text">{{ movieComment }}</p>
          <button 
            v-if="isOwner"
            class="edit-btn" 
            @click="startEditing"
          >수정</button>
        </div>
        
        <div v-else-if="isOwner" class="review-input">
        <textarea 
          v-model="review" 
          placeholder="오늘 하루는 어땠나요? 영화와 함께한 순간을 기록해보세요..."
          maxlength="200"
        ></textarea>
      </div>
      </div>

      <div class="modal-footer">
        <button class="detail-btn" @click="goToDetail">상세정보 보기</button>
        <div v-if="isOwner" class="action-buttons">
          <button 
            v-if="isEditing || !existingReview" 
            class="submit-btn" 
            @click="submitReview"
          >
            {{ existingReview ? '수정' : '저장' }}
          </button>
          <button 
            v-if="isEditing" 
            class="cancel-btn" 
            @click="cancelEdit"
          >
            취소
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const store = useCounterStore()

const props = defineProps({
  show: Boolean,
  movieId: Number,
  movieTitle: String,
  moviePoster: String,
  movieComment: String
})

// existingReview를 movieComment로 사용
const existingReview = computed(() => props.movieComment)
const emit = defineEmits(['close', 'submit', 'update:movieComment', 'data-updated'])
const review = ref('')
const isEditing = ref(false)

// 현재 사용자가 리뷰 작성자인지 확인
const isOwner = computed(() => {
  return store.userKey
  === route.params.userName
})

onMounted(() => {
  review.value = props.existingReview || ''
})

const startEditing = () => {
  if (!isOwner.value) return
  isEditing.value = true
  review.value = props.existingReview
}

const cancelEdit = () => {
  if (!isOwner.value) return
  isEditing.value = false
  review.value = props.existingReview
}
const comment = computed({
  get: () => props.movieComment,
  set: (value) => emit('update:movieComment', value)
})
const submitReview = async () => {
  if (!isOwner.value) return
  try {
    const method = 'post'
    
    await axios[method](
      `${store.API_URL}/movies/day-diary/`,
      {
        tmdb_id: props.movieId,
        comment: review.value
      },
      {
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    
    // 성공 메시지 표시
    alert('새로운 일기가 저장되었습니다.')
    
    // 리뷰 업데이트 이벤트 발생
    emit('update:movieComment', review.value)
    emit('submit', {
      movieId: props.movieId,
      review: review.value
    })
    emit('data-updated')
    isEditing.value = false

    // 마지막으로 페이지 새로고침
    window.location.reload()
    
  } catch (error) {
    console.error('리뷰 저장/수정 실패:', error)
    alert('리뷰 저장/수정에 실패했습니다. 다시 시도해주세요.')
  }
}
const goToDetail = () => {
  router.push(`/movie/${props.movieId}`)
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #1a1f2c;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.movie-info {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.movie-poster {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.movie-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: #ffffff;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  border-bottom: 1px solid #2c3e50;
  padding-bottom: 12px;
}

.modal-header h3 {
  color: #ffffff;
  font-size: 1.6rem;
}

.review-display {
  background: #2c3e50;
  padding: 20px;
  border-radius: 8px;
  position: relative;
  margin-bottom: 20px;
}

.review-text {
  margin-bottom: 15px;
  color: #ffffff;
  line-height: 1.5;
}

.edit-btn {
  position: absolute;
  right: 12px;
  top: 12px;
  background: #e31c1c;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background: #c41818;
}

.modal-body textarea {
  width: 100%;
  min-height: 120px;
  border: 1px solid #2c3e50;
  border-radius: 8px;
  resize: vertical;
  background: #2c3e50;
  color: #ffffff;
  font-size: 1rem;
}

.modal-body textarea::placeholder {
  color: #8795a1;
}

.modal-footer {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #2c3e50;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

button {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.submit-btn {
  background: #e31c1c;
  color: white;
}

.submit-btn:hover {
  background: #c41818;
}

.cancel-btn {
  background: #4a5568;
  color: white;
}

.cancel-btn:hover {
  background: #2d3748;
}

.detail-btn {
  background: #2c3e50;
  color: white;
}

.detail-btn:hover {
  background: #1a2633;
}

.close-btn {
  background: none;
  font-size: 1.8rem;
  color: #ffffff;
  padding: 0;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}
</style>