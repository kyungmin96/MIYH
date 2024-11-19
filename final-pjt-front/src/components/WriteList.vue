<template>
  <div class="write-list">
    <h1>작성 글 목록</h1>
    <div class="write-content">
      <WriteListitem
        v-for="write in store.writes"
        :key="write.id"
        :write="write" 
      />
    </div>
  </div>
</template>

<script setup>
import WriteListitem from '@/components/WriteListitem.vue';
import { useCounterStore } from '@/stores/counter';
const store = useCounterStore()
</script>

<style scoped>
.write-list {
  width: 33%;
  height: 40vh; /* 이전 컴포넌트와 동일한 높이 */
  border: 1px solid #ccc;
  padding: 15px;
}

.write-content {
  border: 1px solid #ccc; /* 경계선 추가 (선택사항) */
  border-radius: 8px; /* 모서리 둥글게 (선택사항) */
  height: calc(80% - 50px); /* h1 높이를 고려하여 조정 */
  overflow-y: auto; /* 세로 스크롤만 표시 */
  overflow-x: hidden; /* 가로 스크롤 숨김 */
}

/* 스크롤바 스타일링 (선택사항) */
.write-content::-webkit-scrollbar {
  width: 8px;
}

.write-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.write-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.write-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>