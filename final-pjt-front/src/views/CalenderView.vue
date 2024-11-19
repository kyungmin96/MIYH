<template>
  <div class="calendar-container">
    <div class="calender-recommend">
      <RecommendView />
      <PopulerView />
    </div>
    <FullCalendar 
      :options="calendarOptions"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import timeGridPlugin from '@fullcalendar/timegrid'
import poster1 from '../image/TMZ-223.jpg'
import poster2 from '../image/TMY-104.jpg'
import RecommendView from '@/components/RecommendView.vue'
import PopulerView from '@/components/PopulerView.vue'

const events = [
  {
    start: '2024-11-18',
    allDay: true,
    display: 'background',
    extendedProps: {
      imageUrl: poster1
    }
  },
  {
    start: '2024-11-20',
    allDay: true,
    display: 'background',
    extendedProps: {
      imageUrl: poster2
    }
  }
]

const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth'
  },
  height: 600,
  aspectRatio: 1.5,
  events: events,
  eventDidMount: (info) => {
    if (info.event.display === 'background') {
      info.el.style.backgroundImage = `url(${info.event.extendedProps.imageUrl})`;
      info.el.style.backgroundSize = 'cover';
      info.el.style.backgroundPosition = 'center';
    }
  },
})
</script>

<style>
.calendar-container {
  max-width: 700px;
  height: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.calender-recommend {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

.fc {
  height: 100% !important;
}

/* 날짜 셀의 높이 설정 */
.fc-daygrid-day {
  height: 100px !important;
}

/* 배경 이미지 이벤트 스타일링 */
.fc-daygrid-day-events {
  margin: 0 !important;
}

.fc-event {
  margin: 0 !important;
  border: none !important;
}

/* 배경 이벤트가 날짜 셀 전체를 채우도록 설정 */
.fc-daygrid-bg-harness {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* 날짜 텍스트를 이미지 위에 보이도록 설정 */
.fc-daygrid-day-top {
  position: relative;
}

/* 날짜 숫자 스타일링 */
.fc-daygrid-day-number {
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.8); 
  padding: 5px !important;
}

/* 오늘 날짜 강조 스타일 */
.fc-day-today {
  background-color: rgba(255, 220, 40, 0.15) !important;
  border: 2px solid #FFD700 !important;
}

/* 오늘 날짜 숫자 스타일 */
.fc-day-today .fc-daygrid-day-number {
  background-color: #FFD700;
  color: #000000;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 5px;
  font-weight: bold;
  text-shadow: none;
}

/* 이미지가 있는 날짜의 경우 오늘 날짜 스타일 조정 */
.fc-day-today.fc-daygrid-day {
  position: relative;
}

.fc-day-today.fc-daygrid-day::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 3px solid #FFD700;
  pointer-events: none;
  z-index: 1;
}

/* 캘린더 헤더 스타일링 */
.fc-header-toolbar {
  margin-bottom: 1.5em !important;
  padding: 10px;
}

.fc-toolbar-title {
  font-size: 1.5em !important;
  font-weight: bold;
}
.fc .fc-bg-event {
  background: var(--fc-bg-event-color);
  opacity: 1 !important; /* 완전 불투명하게 설정 */
}

.fc-button-primary {
  background-color: #4CAF50 !important;
  border-color: #4CAF50 !important;
}

.fc-button-primary:hover {
  background-color: #45a049 !important;
  border-color: #45a049 !important;
}

/* 주말 색상 */
.fc-day-sat {
  color: blue;
}

.fc-day-sun {
  color: red;
}

/* 반응형 스타일 */
@media screen and (max-width: 768px) {
  .calendar-container {
    padding: 0 10px;
  }
  
  .fc-daygrid-day {
    height: 80px !important;
  }
  
  .fc-header-toolbar {
    flex-direction: column;
    gap: 10px;
  }

  .fc-toolbar-title {
    font-size: 1.2em !important;
  }
}
</style>