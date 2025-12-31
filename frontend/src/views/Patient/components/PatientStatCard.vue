<script setup>
const props = defineProps({
  title: String,
  value: Number,
  description: String
});
</script>

<template>
  <div class="stat-card">
    <div class="value">{{ value }}</div>
    <div class="title">{{ title }}</div>
    <div class="desc">{{ description }}</div>
  </div>
</template>

<style scoped>
.stat-card {
  background: white;
  padding: 18px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  text-align: center;
}

.value {
  font-size: 28px;
  font-weight: 800;
  color: #1d3557;
}

.title {
  margin-top: 6px;
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}

.desc {
  margin-top: 4px;
  font-size: 13px;
  color: #64748b;
}
</style>
