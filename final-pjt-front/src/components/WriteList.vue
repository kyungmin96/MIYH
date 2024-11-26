<template>
  <div class="write-list">
    <h2 class="write-title">
      <i class="fas fa-pen"></i>
      작성 글 목록
    </h2>
    <div class="write-content">
      <div v-if="!profileData?.posts?.length" class="no-posts">
        <div class="empty-state">
          <div class="empty-content">
            <i class="fas fa-file-alt"></i>
            <p>작성한 글이 없습니다</p>
          </div>
        </div>
      </div>
      <div v-else class="posts-grid">
        <WriteListitem 
          v-for="post in profileData?.posts"
          :key="post.id"
          :write="post"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import WriteListitem from '@/components/WriteListitem.vue';
import { defineProps } from 'vue';

const props = defineProps({
  profileData: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.write-list {
  width: 100%;
  max-width: 400px;
  max-width: 800px;
  height: 600px;
  margin: 0 auto;
  background: #1a1f2e;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.write-title {
  padding: 1.5rem;
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
  background: #242937;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.write-title i {
  color: #dc1a28;
}

.write-content {
  height: 100%;
  min-height: 200px;
  padding: 1rem;
}

.empty-state {
  height: 100%;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.empty-content i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.empty-content p {
  margin: 0;
  font-size: 0.95rem;
}

.posts-grid {
  display: grid;
  gap: 1rem;
}

.write-content::-webkit-scrollbar {
  width: 4px;
}

.write-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.write-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.write-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>