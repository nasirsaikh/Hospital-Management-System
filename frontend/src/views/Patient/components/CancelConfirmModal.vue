<script setup>
const props = defineProps({
  show: Boolean,
  appointment: Object
});
const emit = defineEmits(["confirm", "close"]);
</script>

<template>
  <div v-if="show" class="backdrop">
    <div class="modal">

      <h3>Cancel Appointment?</h3>

      <p class="info">
        Are you sure you want to cancel your appointment with  
        <span class="doc">{{ appointment?.doctor_name }}</span>?
      </p>

      <div class="actions">
        <button class="cancel" @click="emit('confirm')">Yes, Cancel</button>
        <button class="close" @click="emit('close')">Close</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: #0004;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  width: 360px;
  padding: 22px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}

h3 {
  margin-bottom: 10px;
  color: #1d3557;
}

.info {
  font-size: 14px;
  margin-bottom: 20px;
}
.doc {
  color: #457b9d;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 12px;
}

.cancel {
  background: #e63946;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 8px;
  flex: 1;
}

.close {
  background: #f1f5f9;
  border: none;
  padding: 10px;
  border-radius: 8px;
  flex: 1;
}
</style>
