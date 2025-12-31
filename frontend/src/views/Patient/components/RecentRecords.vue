<script setup>
defineProps({
  items: Array,
  loading: Boolean
});
</script>

<template>
  <div>
    <h2 class="section-title">Recent Medical Records</h2>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="!items || items.length === 0" class="empty">
      No medical records found.
    </div>

    <div class="list" v-else>
      <div class="record" v-for="r in items" :key="r.id">

        <div class="top">
          <div class="name">{{ r.doctor.name }}</div>
          <div class="spec">{{ r.doctor.specialization }}</div>
        </div>

        <div class="date">{{ r.date }}</div>

        <div class="diag">{{ r.diagnosis }}</div>

      </div>
    </div>

  </div>
</template>

<style scoped>
.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #1d3557;
  margin-bottom: 14px;
}

.loading, .empty {
  text-align: center;
  padding: 14px;
  opacity: 0.7;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.record {
  background: white;
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.top {
  display: flex;
  justify-content: space-between;
}

.name {
  font-size: 17px;
  font-weight: 700;
  color: #1d3557;
}

.spec {
  font-size: 13px;
  color: #64748b;
}

.date {
  font-size: 13px;
  color: #475569;
  margin-top: 6px;
}

.diag {
  margin-top: 10px;
  font-size: 14px;
  color: #334155;
  font-weight: 500;
}
</style>
