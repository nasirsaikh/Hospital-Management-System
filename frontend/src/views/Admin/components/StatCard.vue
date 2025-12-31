<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String
});
</script>

<template>
  <div class="card">
    <div class="left">
      <p class="title">{{ title }}</p>
      <h2>{{ value }}</h2>
    </div>

    <div class="icon">
      <i :class="icon"></i>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: white;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  margin: 0;
  font-size: 14px;
  color: #64748b;
}
h2 {
  margin: 6px 0 0;
  font-size: 26px;
}
.icon {
  font-size: 26px;
  color: #1d3557;
}
</style>
