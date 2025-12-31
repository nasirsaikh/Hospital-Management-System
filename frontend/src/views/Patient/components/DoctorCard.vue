<script setup>
const props = defineProps({
  doctor: Object
});
const emit = defineEmits(["details", "book"]);
</script>

<template>
  <div class="card">

    <!-- TOP: Doctor info -->
    <div class="info">
      <img
        class="avatar"
        src="https://picsum.photos/400"
        alt="Doctor"
      />

      <div class="text">
        <div class="name">{{ doctor.name }}</div>
        <div class="spec">{{ doctor.specialization }}</div>
        <div class="fee">₹{{ doctor.fees }} / consultation</div>
      </div>
    </div>

    <!-- BOTTOM: Actions -->
    <div class="actions">
      <button class="btn details" @click="emit('details', doctor)">View Details</button>
      <button class="btn book" @click="emit('book', doctor)">Book Now</button>
    </div>

  </div>
</template>

<style scoped>
.card {
  background: #ffffff;
  padding: 20px;
  border-radius: 20px;
  border: 1px solid #e4eaf2;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: 0.25s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 26px rgba(0,0,0,0.10);
}

/* Doctor Header Section */
.info {
  display: flex;
  gap: 18px;
  align-items: center;
}

.avatar {
  width: 82px;
  height: 82px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e2e8f0;
}

/* Text block */
.text {
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 20px;
  font-weight: 700;
  color: #1d3557;
}

.spec {
  color: #4a6275;
  font-size: 15px;
  margin-top: 2px;
}

.fee {
  margin-top: 6px;
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* Buttons */
.actions {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  padding: 12px 14px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: 0.2s ease;
}

/* Details Button */
.details {
  background: #f1f5f9;
  color: #1d3557;
  border: 1px solid #e2e8f0;
}

.details:hover {
  background: #e2e8f0;
}

/* Book Button */
.book {
  background: #1d3557;
  color: white;
}

.book:hover {
  background: #163049;
}
</style>
