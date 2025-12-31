<script setup>
import { useRouter } from "vue-router";
import { Calendar, FolderOpen, FileText, User } from "lucide-vue-next";

const router = useRouter();
const go = (path) => router.push(path);
</script>

<template>
  <div class="quick-box">

    <div class="item" @click="go('/patient/book')">
      <Calendar class="icon" />
      <div class="label">Book Appointment</div>
    </div>

    <div class="item" @click="go('/patient/appointments')">
      <FolderOpen class="icon" />
      <div class="label">My Appointments</div>
    </div>

    <div class="item" @click="go('/patient/records')">
      <FileText class="icon" />
      <div class="label">Medical Records</div>
    </div>

    <div class="item" @click="go('/patient/profile')">
      <User class="icon" />
      <div class="label">My Profile</div>
    </div>

  </div>
</template>

<style scoped>
.quick-box {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 16px;
}

.item {
  background: white;
  padding: 16px;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  border: 1px solid #e5e7eb;
  cursor: pointer;
  text-align: center;
  transition: transform 0.1s ease;
}

.item:hover {
  transform: translateY(-2px);
}

.icon {
  width: 28px;
  height: 28px;
  stroke: #1d3557;
}

.label {
  margin-top: 8px;
  color: #1d3557;
  font-size: 14px;
  font-weight: 600;
}
</style>
