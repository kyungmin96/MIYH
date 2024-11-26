<template>
  <div class="write-container">
    <form @submit.prevent="submitArticle" class="write-form">
      <div class="form-header">
        <h2>글 작성하기</h2>
      </div>

      <div class="form-group">
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title"
          v-model="title"
          placeholder="제목을 입력하세요"
          required
        >
      </div>

      <div class="form-group">
        <label for="category">카테고리</label>
        <select 
          id="category"
          v-model="category"
          required
        >
          <option value="">카테고리 선택</option>
          <option value="talk">잡담</option>
          <option value="review">리뷰</option>
        </select>
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model="content"
          placeholder="내용을 입력하세요"
          rows="10"
          required
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="button" @click="goBack" class="cancel-btn">취소</button>
        <button type="submit" class="submit-btn">등록</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const router = useRouter()
const store = useCounterStore()

const title = ref('')
const category = ref('')
const content = ref('')

const submitArticle = async () => {
  try {
    const response = await axios.post(
      `${store.API_URL}/community/posts/create/`,
      {
        title: title.value,
        content: content.value,
        category: category.value,
      },
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    )

    if (response.data) {
      alert('글이 성공적으로 등록되었습니다.')
      router.push('/article')
    }
  } catch (error) {
    console.error('글 작성 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push('/login')
    } else {
      alert('글 작성에 실패했습니다. 다시 시도해주세요.')
    }
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.write-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
}

.write-form {
  background: #1a1f2e;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h2 {
  font-size: 1.6rem;
  color: #ffffff;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #ffffff;
}

input, select, textarea {
  width: 100%;
  padding: 0.8rem;
  background: #2a2f3e;
  border: 1px solid #3a3f4e;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #ffffff;
}

textarea {
  resize: vertical;
  min-height: 200px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

button {
  padding: 0.7rem 1.8rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn {
  background-color: #dc1a1a;
  color: white;
}

.submit-btn:hover {
  background-color: #c41717;
}

.cancel-btn {
  background-color: #3a3f4e;
  color: white;
}

.cancel-btn:hover {
  background-color: #2a2f3e;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #dc1a1a;
  box-shadow: 0 0 0 2px rgba(220,26,26,0.2);
}

input::placeholder, textarea::placeholder {
  color: #6c757d;
}

select option {
  background: #2a2f3e;
  color: #ffffff;
}

@media (max-width: 768px) {
  .write-container {
    padding: 1rem;
  }
  
  .write-form {
    padding: 1.25rem;
  }
  
  button {
    padding: 0.7rem 1.4rem;
  }
}
</style>