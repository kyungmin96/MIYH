<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-backdrop" @click.self="closeModal">
      <div class="modal">
        <button class="close-btn" @click="closeModal">×</button>
        <div v-if="videoId" class="video-container">
          <iframe
            :src="videoUrl"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
        <div v-else class="no-trailer">
          <i class="fas fa-film"></i>
          <p>트레일러가 제공되지 않는 영화입니다.</p>
          <button class="close-trailer-btn" @click="closeModal">
            닫기
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue';

const isOpen = ref(false);
const videoId = ref('');

const videoUrl = computed(() => {
  if (!videoId.value) return '';
  
  let id = videoId.value;
  if (videoId.value.includes('youtube.com')) {
    const url = new URL(videoId.value);
    id = url.searchParams.get('v');
  }
  
  return `https://www.youtube.com/embed/${id}?autoplay=1`;
});

const openModal = (id) => {
  videoId.value = id;
  isOpen.value = true;
};

const closeModal = () => {
  isOpen.value = false;
  videoId.value = '';
};

defineExpose({ openModal, closeModal });
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #000;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  position: relative;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.no-trailer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: #ffffff;
}

.no-trailer i {
  font-size: 48px;
  color: #dc1a28;
  margin-bottom: 20px;
}

.no-trailer p {
  font-size: 1.2rem;
  margin-bottom: 25px;
  color: #a0a0a0;
}

.close-trailer-btn {
  padding: 12px 30px;
  background: #dc1a28;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-trailer-btn:hover {
  background: #b91521;
  transform: translateY(-2px);
}

.close-btn {
  position: absolute;
  top: -30px;
  right: -30px;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  z-index: 1001;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>