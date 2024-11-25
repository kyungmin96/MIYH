<template>
  <div class="calendar-container">
    <div class="calender-recommend">
    <RecommendView v-if="recommendMovies" :movieData="recommendMovies"/>
    <PopulerView v-if="popularMovies" :movieData="popularMovies"/>
  </div>
    <div class="calendar-wrapper">
      <FullCalendar 
        :options="calendarOptions"
      />
    </div>
    <ReviewModal
  v-if="showReviewModal"
  :show="showReviewModal"
  :movie-id="selectedMovieId"
  :movie-title="selectedMovieTitle"
  :movie-poster="selectedMoviePoster"
  :movie-comment="selectedMovieComment"
  :selected-date="selectedDate"
  @close="closeReviewModal"
  @data-updated="refetchCalendarData"
/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import timeGridPlugin from '@fullcalendar/timegrid'
import { useCounterStore } from '@/stores/counter'
import RecommendView from '@/components/RecommendView.vue'
import PopulerView from '@/components/PopulerView.vue'
import axios from 'axios'
import ReviewModal from '@/components/ReviewModal.vue'

const router = useRouter()
const route = useRoute()
const store = useCounterStore()
const events = ref(null)
const recommendMovies = ref(null)
const popularMovies = ref(null)
const lastYear = ref(null)
const lastMonth = ref(null)

const selectedDate = ref(null)
const showReviewModal = ref(false)
const selectedMovieId = ref(null)
const selectedMovieTitle = ref(null)
const selectedMoviePoster = ref(null)
const selectedMovieComment =ref(null)
const closeReviewModal = () => {
  showReviewModal.value = false
  // 선택된 날짜 스타일 제거
  document.querySelectorAll('.fc-daygrid-day.selected').forEach(el => {
    el.classList.remove('selected')
  })
  // 상태 초기화
  selectedDate.value = null
  selectedMovieId.value = null
  selectedMovieTitle.value = null
  selectedMoviePoster.value = null
  selectedMovieComment.value =null
}
const fullCalendarRef = ref(null)

const refetchCalendarData = async () => {
  if (lastYear.value && lastMonth.value) {
    await fetchCalendarData(lastYear.value, lastMonth.value)
  }
}

// FullCalendar 강제 새로고침을 위한 함수
const forceCalendarRefresh = () => {
  if (fullCalendarRef.value) {
    const calendarApi = fullCalendarRef.value.getApi()
    calendarApi.refetchEvents()
  }
}

// calendarOptions 수정
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
  initialDate: new Date().toISOString(),
  initialView: 'dayGridMonth',
  firstDay: 1,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth'
  },
  height: 1200,
  aspectRatio: 2,
  events: events,
  handleWindowResize: true,
  progressiveEventRendering: true,
  rerenderDelay: 100,
  validRange: {
    start: '2024-01-01',
    end: '2025-12-31'
  },
  lazyFetching: false,
  loading: (isLoading) => {},
  // 하나의 eventDidMount만 유지
  eventDidMount: (info) => {
    if (info.event.display === 'background') {
      const cell = info.el
      cell.style.backgroundImage = `url(${info.event.extendedProps.poster_path})`
      cell.style.backgroundSize = 'cover'
      cell.style.backgroundPosition = 'center'
      cell.style.opacity = '0.8'
      cell.style.cursor = 'pointer'
      
      cell.addEventListener('click', () => {
        // 선택된 날짜 저장
        selectedDate.value = info.event.start
        
        // 선택된 날짜 스타일링
        const dateCell = cell.closest('.fc-daygrid-day')
        if (dateCell) {
          // 이전 선택된 날짜의 스타일 제거
          document.querySelectorAll('.fc-daygrid-day.selected').forEach(el => {
            el.classList.remove('selected')
          })
          // 새로 선택된 날짜에 스타일 추가
          dateCell.classList.add('selected')
        }

        // 영화 정보 설정
        selectedMovieId.value = Number(info.event.id)
        selectedMovieTitle.value = info.event.title
        selectedMoviePoster.value = info.event.extendedProps.poster_path
        selectedMovieComment.value = info.event.extendedProps.comment
        // 모달 열기
        showReviewModal.value = true
      })
    }
  },
  // 날짜 변경 핸들러
  datesSet: async (dateInfo) => {
  // 달력의 현재 표시된 날짜 정보 가져오기
  const viewTitle = document.querySelector('.fc-toolbar-title').textContent
  
  // "November 2024" 형식의 문자열에서 년도와 월 추출
  const [monthName, year] = viewTitle.split(' ')
  
  // 월 이름을 숫자로 변환
  const monthNames = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
  }
  
  const month = monthNames[monthName]
  

  
  // 이전 상태와 비교
  if (lastYear.value !== Number(year) || lastMonth.value !== month) {
    // 상태 업데이트
    lastYear.value = Number(year)
    lastMonth.value = month
    
    // 이전 이벤트 초기화
    events.value = []
    
    try {
      await fetchCalendarData(Number(year), month)
    } catch (error) {
      console.error('데이터 로드 실패:', error)
    }
  }
}
})
const fetchCalendarData = async (year, month) => {
  try {
    const response = await axios.get(
      `${store.API_URL}/movies/calendar/${route.params.userName}/`,
      {
        params: {
          year: year,
          month: month
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    
    if (response.data && Array.isArray(response.data)) {
      events.value = response.data.map(event => ({
        id: event.id,
        title: event.title,
        start: event.date,
        display: 'background',
        extendedProps: {
          poster_path: `https://image.tmdb.org/t/p/original${event.poster_path}`,
          comment: event.comment
        }
      }))
      
      // 달력 강제 새로고침
      forceCalendarRefresh()
    }
  } catch (error) {
    console.error('캘린더 데이터 로드 실패:', error)
  }
}


const fetchRecommendations = async () => {
  try {
    const { latitude, longitude } = store.userLocation

    const response = await axios.get(
      `${store.API_URL}/movies/recommendations/`,
      {
        params: {
          latitude: latitude,
          longitude: longitude
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      }
    )
    if (response.data.recommendations && Array.isArray(response.data.recommendations)) {
      
      recommendMovies.value = response.data.recommendations[0] // 추천 영화
      popularMovies.value = response.data.recommendations[1]   // 인기 영화
    }
  } catch (error) {
    console.error('추천 영화 로드 실패:', error)
  }
}

onMounted(async () => {
  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  
  await fetchRecommendations()
  
  // 현재 날짜로 초기 데이터 로드
  const today = new Date()
  const currentYear = today.getFullYear()
  const currentMonth = today.getMonth() + 1
  
  // 초기 상태 설정
  lastYear.value = currentYear
  lastMonth.value = currentMonth
  
  await fetchCalendarData(currentYear, currentMonth)
})
</script>

<style>
.calendar-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.calender-recommend {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.calendar-wrapper {
  background: rgba(28, 33, 46, 0.95);
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.fc {
  background: transparent;
  color: #ffffff;
}

/* 캘린더 헤더 스타일링 */
.fc-header-toolbar {
  padding: 15px !important;
  margin-bottom: 20px !important;
}

.fc-toolbar-title {
  color: #ffffff !important;
  font-size: 1.5rem !important;
  font-weight: 600 !important;
}

/* 버튼 스타일링 */
.fc-button-primary {
  background: linear-gradient(145deg, #e50914, #b2070f) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 8px 16px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

.fc-button-primary:hover {
  background: linear-gradient(145deg, #f40612, #e50914) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3) !important;
}

/* 날짜 셀 스타일링 */
.fc-daygrid-day {
  min-height: 150px !important; /* 높이 증가 */
  height: 150px !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.fc-daygrid-day-number {
  color: #ffffff !important;
  font-weight: 500 !important;
  padding: 8px !important;
}

/* 오늘 날짜 스타일 */
.fc-day-today {
  background: rgba(229, 9, 20, 0.1) !important;
}

.fc-day-today .fc-daygrid-day-number {
  background: #e50914;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 5px;
}

/* 주말 색상 */
.fc-day-sat .fc-daygrid-day-number {
  color: #4a90e2 !important;
}

.fc-day-sun .fc-daygrid-day-number {
  color: #e50914 !important;
}

/* 이벤트 스타일링 */
.fc-bg-event {
  opacity: 0.8 !important;
  border-radius: 8px !important;
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .calendar-container {
    padding: 0 15px;
    margin: 20px auto;
  }

  .calender-recommend {
    flex-direction: column;
  }

  .calendar-wrapper {
    padding: 15px;
  }

  .fc-daygrid-day {
    height: 80px !important;
  }

  .fc-header-toolbar {
    flex-direction: column;
    gap: 10px;
    padding: 10px !important;
  }

  .fc-toolbar-title {
    font-size: 1.2rem !important;
  }

  .fc-button-primary {
    padding: 6px 12px !important;
    font-size: 0.9rem !important;
  }
}
</style>