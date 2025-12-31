<script setup>
const model = defineModel();
</script>

<template>
  <div class="filters">
    <button
      :class="model === 'all' ? 'active' : ''"
      @click="model = 'all'"
    >
      All
    </button>

    <button
      :class="model === 'pending' ? 'active' : ''"
      @click="model = 'pending'"
    >
      Pending
    </button>

    <button
      :class="model === 'confirmed' ? 'active' : ''"
      @click="model = 'confirmed'"
    >
      Confirmed
    </button>

    <button
      :class="model === 'completed' ? 'active' : ''"
      @click="model = 'completed'"
    >
      Completed
    </button>

    <button
      :class="model === 'cancelled' ? 'active' : ''"
      @click="model = 'cancelled'"
    >
      Cancelled
    </button>
  </div>
</template>

<style scoped>
.filters {
  display: flex;
  gap: 12px;
  padding-bottom: 12px;
}

button {
  padding: 8px 14px;
  border-radius: 20px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  cursor: pointer;
}

button.active {
  background: #1d3557;
  border-color: #1d3557;
  color: white;
}
</style>
