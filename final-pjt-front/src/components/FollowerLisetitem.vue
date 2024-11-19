<template>
  <div>
<p>{{ fowller.name }}</p>
<p>{{ fowller.count }}</p>
<hr>
  </div>
</template>

<script setup>
defineProps({
  fowller: Object
})
</script>

<style scoped>

</style>