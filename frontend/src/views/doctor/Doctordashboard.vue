<script setup>
import { ref, onMounted } from "vue";
import doctorDashboardAPI from "@/api/doctor/dashboard";

const loading = ref(true);
const stats = ref({});
const todayAvailability = ref([]);
const upcomingAppointments = ref([]);
const doctorInfo = ref({});

const load = async () => {
  try {
    const res = await doctorDashboardAPI.getDashboard();

    doctorInfo.value = res.data.doctor;
    stats.value = res.data.stats;
    todayAvailability.value = res.data.today_availability;
    upcomingAppointments.value = res.data.upcoming_appointments;

  } catch (e) {
    console.error("Failed to load doctor dashboard:", e);
  }
  loading.value = false;
};

onMounted(load);
</script>

<template>
  <div class="page">


    <div class="header">
      <div class="left">
        <h1 class="title">Doctor Dashboard</h1>
        <p class="welcome">Welcome back, <strong>{{ doctorInfo.full_name }}</strong></p>
      </div>

      <div class="profile-box">
        <div class="avatar">{{ doctorInfo.full_name?.[0] }}</div>
        <div class="info">
          <p class="name">{{ doctorInfo.full_name }}</p>
          <p class="email">{{ doctorInfo.email }}</p>
        </div>
      </div>
    </div>


    <div v-if="loading" class="loader-wrap">
      <div class="loader"></div>
      <span>Loading dashboard...</span>
    </div>


    <div v-else>


      <div class="stats">
        <div class="stat-card">
          <h2 class="num">{{ stats.total_patients }}</h2>
          <p class="label">Total Patients</p>
        </div>

        <div class="stat-card">
          <h2 class="num">{{ stats.upcoming_appointments }}</h2>
          <p class="label">Upcoming Appointments</p>
        </div>

        <div class="stat-card status" :class="stats.is_verified ? 'verified' : 'pending'">
          <h2 class="num">{{ stats.is_verified ? 'Verified' : 'Pending' }}</h2>
          <p class="label">Verification</p>
        </div>
      </div>


      <div class="section">
        <h2 class="section-title">Today’s Availability</h2>

        <div v-if="todayAvailability.length === 0" class="empty">
          No availability set for today.
        </div>

        <div v-else class="availability">
          <div v-for="slot in todayAvailability" :key="slot.id" class="slot">
            <span class="slot-type">{{ slot.slot_type.toUpperCase() }}</span>
            <span class="slot-time">{{ slot.start_time }} – {{ slot.end_time }}</span>
          </div>
        </div>
      </div>


      <div class="section">
        <h2 class="section-title">Upcoming Appointments</h2>

        <div v-if="upcomingAppointments.length === 0" class="empty">
          No upcoming appointments.
        </div>

        <table v-else class="table">
          <thead>
            <tr>
              <th>Patient</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="a in upcomingAppointments" :key="a.id">
              <td>{{ a.patient_name }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>
                <span class="badge" :class="a.status">{{ a.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 1200px;
  margin: auto;

}


.header {
  background: #13293d;
  color: white;
  padding: 26px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 28px;
  font-weight: 700;
}

.welcome {
  margin-top: 4px;
  color: #d6e4f0;
}

.profile-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #e8eef5;
  color: #13293d;
  display: grid;
  place-items: center;
  font-size: 22px;
  font-weight: 700;
}

.info .name {
  font-weight: 700;
}

.info .email {
  opacity: 0.8;
}


.loader-wrap {
  margin-top: 40px;
  text-align: center;
}

.loader {
  width: 30px;
  height: 30px;
  border: 4px solid #d0d5dd;
  border-top-color: #13293d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 18px;
  margin-top: 28px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.num {
  font-size: 32px;
  font-weight: 700;
  color: #13293d;
}

.label {
  color: #6b7280;
  margin-top: 4px;
}


.status.verified {
  background: #d1fae5;
  color: #065f46;
}

.status.pending {
  background: #ffe4e6;
  color: #b91c1c;
}


.section {
  margin-top: 40px;
}

.section-title {
  font-size: 20px;
  color: #13293d;
  margin-bottom: 14px;
}


.availability {
  background: white;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.slot {
  display: flex;
  justify-content: space-between;
  padding: 12px 8px;
  border-bottom: 1px solid #eef1f4;
}

.slot:last-child {
  border-bottom: none;
}

.slot-type {
  font-weight: 700;
  color: #13293d;
}

.slot-time {
  color: #556575;
}


.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.table th {
  background: #f0f3f7;
  padding: 14px;
  text-align: left;
}

.table td {
  padding: 14px;
  border-bottom: 1px solid #eef1f4;
}


.badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  text-transform: capitalize;
  color: white;
}

.badge.pending {
  background: #facc15;
  color: #854d0e;
}

.badge.confirmed {
  background: #0ea5e9;
}

.badge.completed {
  background: #22c55e;
}

.badge.cancelled {
  background: #dc2626;
}


.empty {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}
</style>
