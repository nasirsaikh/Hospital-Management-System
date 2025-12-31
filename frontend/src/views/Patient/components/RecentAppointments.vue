<script setup>
defineProps({
  items: Array,
  loading: Boolean
});
</script>

<template>
  <div>
    <h2 class="section-title">Recent Appointments</h2>

    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-else-if="!items || items.length === 0" class="empty">
      No recent appointments.
    </div>

    <div class="list" v-else>

      <div class="card" v-for="a in items" :key="a.id">

        <div class="top">
          <div class="name">{{ a.doctor.name }}</div>
          <div class="spec">{{ a.doctor.specialization }}</div>
        </div>

        <div class="row">
          <span class="label">Date:</span> {{ a.date }}
        </div>

        <div class="row">
          <span class="label">Time:</span> {{ a.time }}
        </div>

        <span class="status" :class="a.status.toLowerCase()">
          {{ a.status }}
        </span>

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

.card {
  background: white;
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.row {
  margin-top: 6px;
  font-size: 14px;
}

.label {
  font-weight: 600;
  color: #475569;
}

.status {
  margin-top: 10px;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
  text-transform: capitalize;
}

.status.pending {
  background: #fff4d6;
  color: #b45309;
}

.status.confirmed {
  background: #dcfce7;
  color: #15803d;
}

.status.completed {
  background: #dbeafe;
  color: #1e3a8a;
}

.status.cancelled {
  background: #fee2e2;
  color: #b91c1c;
}
</style>
