<script setup>
defineProps({ title: String });
</script>

<template>
  <section class="section">
    <h3>{{ title }}</h3>
    <slot></slot>
  </section>
</template>

<style scoped>
.section {
  background: white;
  border: 1px solid #e2e8f0;
  padding: 20px;
  border-radius: 14px;
  margin-bottom: 25px;
}
h3 {
  margin: 0 0 14px;
  font-size: 18px;
}
</style>
