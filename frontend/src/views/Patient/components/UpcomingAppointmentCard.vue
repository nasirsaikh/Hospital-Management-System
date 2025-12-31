<script setup>
const props = defineProps({
  appointment: Object,
  loading: Boolean,
});
</script>

<template>
  <div class="card">


    <div v-if="loading" class="loading-wrap">
      <div class="loader"></div>
      <p>Loading appointment...</p>
    </div>


    <div v-else-if="!appointment" class="empty">
      No upcoming appointment scheduled.
    </div>


    <div v-else class="content">
      <h3 class="label">Next Appointment</h3>

      <div class="doctor-block">
        <div class="doc-name">{{ appointment.doctor.name }}</div>
        <div class="doc-spec">{{ appointment.doctor.specialization }}</div>
      </div>

      <div class="info">
        <div class="row">
          <span>Date</span>
          <strong>{{ appointment.date }}</strong>
        </div>

        <div class="row">
          <span>Time</span>
          <strong>{{ appointment.time }}</strong>
        </div>

        <div class="row">
          <span>Status</span>
          <span class="status" :class="appointment.status">
            {{ appointment.status }}
          </span>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
}


.loading-wrap {
  text-align: center;
}

.loader {
  width: 26px;
  height: 26px;
  border: 3px solid #d1d5db;
  border-top-color: #1d3557;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty {
  text-align: center;
  color: #64748b;
  padding: 20px;
}


.label {
  font-size: 18px;
  font-weight: 700;
  color: #1d3557;
  margin-bottom: 12px;
}

.doctor-block {
  margin-bottom: 16px;
}

.doc-name {
  font-size: 18px;
  font-weight: 700;
  color: #1d3557;
}

.doc-spec {
  font-size: 14px;
  color: #64748b;
}

.info {
  background: #f8fafc;
  padding: 14px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.row:last-child {
  margin-bottom: 0;
}

.status {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  text-transform: capitalize;
  color: white;
}

.status.pending {
  background: #fbbf24;
}

.status.confirmed {
  background: #0ea5e9;
}

.status.completed {
  background: #16a34a;
}

.status.cancelled {
  background: #dc2626;
}
</style>
