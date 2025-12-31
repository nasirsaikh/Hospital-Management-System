<script setup>
import { computed } from "vue";

const props = defineProps({
  show: Boolean,
  appointment: Object,
});

const emits = defineEmits(["close"]);

const formattedStatus = computed(() => {
  if (!props.appointment) return "";
  return props.appointment.status.charAt(0).toUpperCase() + props.appointment.status.slice(1);
});
</script>

<template>
  <div v-if="show" class="modal-bg">
    <div class="modal">

      <h2 class="title">Appointment Details</h2>

      <button class="close-btn" @click="$emit('close')">×</button>

      <div v-if="appointment" class="content">

        <div class="section">
          <h3>Patient Information</h3>
          <p><strong>Name:</strong> {{ appointment.patient.name }}</p>
          <p><strong>Age:</strong> {{ appointment.patient.age }}</p>
          <p><strong>Gender:</strong> {{ appointment.patient.gender }}</p>
          <p><strong>Phone:</strong> {{ appointment.patient.phone }}</p>
        </div>

        <div class="section">
          <h3>Appointment Details</h3>
          <p><strong>Date:</strong> {{ appointment.date }}</p>
          <p><strong>Time:</strong> {{ appointment.time }}</p>
          <p><strong>Status:</strong> {{ formattedStatus }}</p>
        </div>

      </div>

      <div class="footer">
        <button class="close-footer" @click="$emit('close')">Close</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal {
  background: white;
  width: 470px;
  border-radius: 12px;
  padding: 20px 24px;
  position: relative;
  animation: pop 0.2s ease;
}

@keyframes pop {
  from {
    transform: scale(0.9);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 14px;
  font-size: 26px;
  background: none;
  border: none;
  cursor: pointer;
}

.title {
  margin-bottom: 14px;
  text-align: center;
}

.section {
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
}

.section h3 {
  font-size: 17px;
  margin-bottom: 6px;
  font-weight: 600;
  color: #1d3557;
}

.footer {
  display: flex;
  justify-content: flex-end;
}

.close-footer {
  padding: 8px 14px;
  background: #1d3557;
  color: white;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}
</style>
