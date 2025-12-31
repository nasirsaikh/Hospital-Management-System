<script setup>
import { ref, watch, computed } from "vue";

const props = defineProps({
  show: Boolean,
  doctor: Object,
  slots: Array,
});

const emit = defineEmits(["close", "select-slot"]);


const selected = ref(null);

watch(
  () => props.show,
  (v) => {
    document.body.style.overflow = v ? "hidden" : "";
    if (!v) selected.value = null;
  }
);


const confirmBooking = () => {
  if (selected.value) emit("select-slot", selected.value);
};

</script>

<template>
  <div v-if="show" class="overlay">
    <div class="modal">

      <button class="close-btn" @click="$emit('close')">×</button>

      <h2 class="title">Book Appointment</h2>
      <p class="subtitle">Choose a slot with {{ doctor?.full_name }}</p>

      <!-- Slots -->
      <div class="slots-container">
        <div v-for="s in slots" :key="s.date + s.time" class="slot-card"
          :class="{ selected: selected?.date === s.date && selected?.time === s.time }" @click="selected = s">
          <div class="slot-date">{{ s.date }}</div>
          <div class="slot-time">{{ s.time }}</div>
        </div>

        <p v-if="slots.length === 0" class="empty">No available slots</p>
      </div>

      <!-- Confirm appears only when selected -->
      <transition name="slide-up">
        <button v-if="selected" class="confirm-btn" @click="confirmBooking">
          Confirm Appointment
        </button>
      </transition>

      <button class="close-bottom" @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 120;
}


.modal {
  background: white;
  width: 480px;
  max-height: 85vh;
  padding: 28px;
  border-radius: 18px;
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.18);
  position: relative;
  display: flex;
  flex-direction: column;
  animation: popup 0.25s ease;
}

@keyframes popup {
  from {
    transform: scale(0.92);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  right: 16px;
  top: 12px;
  font-size: 26px;
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.7;
}


.title {
  font-size: 22px;
  font-weight: 700;
  color: #1d3557;
  text-align: center;
  margin-bottom: 6px;
}

.subtitle {
  text-align: center;
  color: #64748b;
  margin-bottom: 18px;
}


.slots-container {
  flex: 1;
  overflow-y: auto;
  padding-right: 6px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 14px;
}


.slot-card {
  padding: 14px;
  border-radius: 14px;
  background: #f1f5f9;
  border: 1px solid #dce3eb;
  cursor: pointer;
  transition: .2s;
  min-height: 70px;
}

.slot-card:hover {
  background: #e6f0ff;
  border-color: #1d3557;
  transform: translateY(-2px);
}


.slot-card.selected {
  background: #dce8ff;
  border-color: #1d3557;
  box-shadow: 0 0 0 2px #1d3557 inset;
}


.confirm-btn {
  margin-top: 16px;
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 16px;
  background: #2563eb;
  color: white;
  cursor: pointer;
  font-weight: 600;
}


.close-bottom {
  margin-top: 14px;
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: #1d3557;
  color: white;
  cursor: pointer;
  font-weight: 600;
}


.slide-up-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.slide-up-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.slide-up-enter-active {
  transition: .25s ease;
}
</style>
