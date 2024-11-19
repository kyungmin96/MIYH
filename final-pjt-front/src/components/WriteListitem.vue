<template>
  <div>
<p>{{ write.title }}</p>
<p>{{ write.content }}</p>
<hr>
  </div>
</template>

<script setup>
defineProps({
  write: Object
})
</script>

<style scoped>

</style>