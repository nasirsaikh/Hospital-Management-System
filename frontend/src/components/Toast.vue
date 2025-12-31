<script setup>
import { useToastStore } from "@/store/toast";

const toast = useToastStore();
</script>

<template>
  <div class="toast-container">
    <div v-for="t in toast.toasts" :key="t.id" class="toast" :class="t.type">
      {{ t.message }}
    </div>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}

.toast {
  padding: 12px 18px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  animation: fadeIn 0.3s ease-out;
  min-width: 220px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.toast.success {
  background: #16a34a;
}

.toast.error {
  background: #dc2626;
}

.toast.info {
  background: #2563eb;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
