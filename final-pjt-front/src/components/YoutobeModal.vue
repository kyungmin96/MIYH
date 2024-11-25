<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-backdrop" @click.self="closeModal">
      <div class="modal">
        <button class="close-btn" @click="closeModal">×</button>
        <div class="video-container">
          <iframe
            :src="videoUrl"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref,computed  } from 'vue';

const isOpen = ref(false);
const videoId = ref('');

const videoUrl = computed(() => {
  // YouTube 동영상 ID만 추출하여 사용
  return `https://www.youtube.com/embed/soCtsN0JYUg?autoplay=1`;
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