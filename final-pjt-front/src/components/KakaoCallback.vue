<template>
  <div class="kakao-callback">
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      <p>카카오 로그인 처리 중...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const store = useCounterStore();

onMounted(async () => {
  const code = route.query.code;
  if (code) {
    await store.handleKakaoCallback(code);
  }
});
</script>

<style scoped>
.kakao-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #1a1f2c;
}

.loading {
  text-align: center;
  color: #ffffff;
}

.loading i {
  font-size: 2rem;
  color: #FEE500;
  margin-bottom: 1rem;
}

.loading p {
  font-size: 1.1rem;
}
</style>