<script setup>
const props = defineProps({
  appointment: { type: Object, required: true }
});
const emit = defineEmits(["cancel"]);
</script>

<template>
  <div class="card">
    <div class="top">
      <div>
        <div class="doctor">{{ appointment.doctor_name }}</div>
        <div class="special">{{ appointment.specialization }}</div>
      </div>

      <div class="status" :class="appointment.status.toLowerCase()">
        {{ appointment.status }}
      </div>
    </div>

    <div class="details">
      <span><strong>Date:</strong> {{ appointment.date }}</span>
      <span><strong>Time:</strong> {{ appointment.time }}</span>
    </div>

    <button
      v-if="appointment.status !== 'cancelled' && appointment.status !== 'completed'"
      class="cancel-btn"
      @click="emit('cancel', appointment)"
    >
      Cancel Appointment
    </button>
  </div>
</template>

<style scoped>
.card {
  background: white;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #e4e7eb;
  box-shadow: 0 3px 10px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.doctor {
  font-size: 18px;
  font-weight: 700;
  color: #1d3557;
}

.special {
  font-size: 13px;
  color: #64748b;
}

.status {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status.pending {
  background: #fff7d6;
  color: #b7791f;
}
.status.confirmed {
  background: #d1fae5;
  color: #15803d;
}
.status.completed {
  background: #e0e7ff;
  color: #3730a3;
}
.status.cancelled {
  background: #ffe4e6;
  color: #b91c1c;
}

.details {
  display: flex;
  gap: 18px;
  font-size: 14px;
  color: #475569;
}

.cancel-btn {
  align-self: start;
  background: #e63946;
  color: white;
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}
</style>
