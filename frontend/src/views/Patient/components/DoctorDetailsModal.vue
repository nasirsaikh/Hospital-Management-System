<script setup>
const props = defineProps({
  show: Boolean,
  doctor: Object
});
const emit = defineEmits(["close", "book"]);
</script>

<template>
  <div v-if="show" class="backdrop">
    <div class="modal">

      <button class="close-btn" @click="emit('close')">×</button>

      <img
        class="avatar"
        src="https://picsum.photos/200/300"
      />

      <h2 class="name">{{ doctor?.full_name }}</h2>
      <p class="spec">{{ doctor?.specialization }}</p>

      <div class="bio" v-if="doctor?.bio">
        {{ doctor.bio }}
      </div>

      <div class="rows">
        <div class="row">
          <strong>Experience:</strong> {{ doctor?.experience }} yrs
        </div>
        <div class="row">
          <strong>Qualification:</strong> {{ doctor?.qualification }}
        </div>
        <div class="row">
          <strong>Fee:</strong> ₹{{ doctor?.fees }}
        </div>
      </div>

      <button class="book-btn" @click="emit('book', doctor)">Book Appointment</button>

    </div>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: #0003;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  width: 360px;
  padding: 24px;
  border-radius: 16px;
  position: relative;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 16px;
  top: 12px;
  font-size: 20px;
  border: none;
  background: transparent;
  cursor: pointer;
}

.avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
}

.name {
  color: #1d3557;
  font-size: 22px;
  font-weight: 700;
}

.spec {
  color: #475569;
  font-size: 14px;
  margin-bottom: 12px;
}

.bio {
  font-size: 14px;
  color: #475569;
  margin-bottom: 16px;
}

.rows {
  text-align: left;
  margin-bottom: 18px;
}

.row {
  margin-bottom: 6px;
  font-size: 14px;
}

.book-btn {
  background: #1d3557;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 10px;
  width: 100%;
  cursor: pointer;
}
</style>
