<script setup>
import { ref, onMounted } from "vue";
import adminAPI from "@/api/admin/admin";

const loading = ref(true);

const stats = ref({
  doctors: 0,
  patients: 0,
  appointments: 0,
  completed: 0,
  pendingVerifications: 0,
  today: 0,
});

const recentAppointments = ref([]);

onMounted(async () => {
  try {
    const res = await adminAPI.dashboard();
    stats.value = res.data.stats;
    recentAppointments.value = res.data.recentAppointments;
  } catch (err) {
    console.error("Admin dashboard error:", err);
  }
  loading.value = false;
});
</script>

<template>
  <div class="page">


    <div class="header">
      <div>
        <h1 class="title">Admin Dashboard</h1>
        <p class="subtitle">Overview of the healthcare platform performance.</p>
      </div>
    </div>


    <div v-if="loading" class="loader-wrap">
      <div class="loader"></div>
      <span>Loading dashboard...</span>
    </div>


    <div v-else>


      <div class="stats-grid">

        <div class="stat-card blue">
          <div class="stat-value">{{ stats.doctors }}</div>
          <div class="stat-label">Doctors</div>
        </div>

        <div class="stat-card teal">
          <div class="stat-value">{{ stats.patients }}</div>
          <div class="stat-label">Patients</div>
        </div>

        <div class="stat-card purple">
          <div class="stat-value">{{ stats.appointments }}</div>
          <div class="stat-label">Total Appointments</div>
        </div>

        <div class="stat-card green">
          <div class="stat-value">{{ stats.completed }}</div>
          <div class="stat-label">Completed</div>
        </div>

        <div class="stat-card orange">
          <div class="stat-value">{{ stats.pendingVerifications }}</div>
          <div class="stat-label">Pending Verifications</div>
        </div>

        <div class="stat-card red">
          <div class="stat-value">{{ stats.today }}</div>
          <div class="stat-label">Today’s Appointments</div>
        </div>

      </div>


      <div class="section">
        <h2 class="section-title">Recent Appointments</h2>

        <div v-if="recentAppointments.length === 0" class="empty">
          No recent appointments.
        </div>

        <table v-else class="table">
          <thead>
            <tr>
              <th>Doctor</th>
              <th>Patient</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in recentAppointments" :key="item.id">
              <td>{{ item.doctor }}</td>
              <td>{{ item.patient }}</td>
              <td>{{ item.date }}</td>
              <td>{{ item.time }}</td>
              <td>
                <span class="badge" :class="item.status">
                  {{ item.status }}
                </span>
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
  max-width: 1250px;
  margin: auto;
}


.header {
  background: linear-gradient(135deg, #1d3557, #406e9f);
  padding: 26px 34px;
  border-radius: 14px;
  color: white;
  margin-bottom: 32px;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.12);
}

.title {
  font-size: 28px;
  font-weight: 700;
}

.subtitle {
  opacity: 0.9;
  margin-top: 4px;
  font-size: 15px;
}


.loader-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-top: 40px;
}

.loader {
  width: 30px;
  height: 30px;
  border: 4px solid #cbd5e1;
  border-top-color: #1d3557;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 18px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 18px;
  border-radius: 12px;
  text-align: center;
  color: white;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
}

.stat-label {
  margin-top: 6px;
  font-size: 14px;
  opacity: 0.85;
}


.blue {
  background: #3b82f6;
}

.teal {
  background: #14b8a6;
}

.purple {
  background: #8b5cf6;
}

.green {
  background: #22c55e;
}

.orange {
  background: #f59e0b;
}

.red {
  background: #ef4444;
}


.section-title {
  font-size: 20px;
  margin-bottom: 16px;
  color: #1d3557;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.table th {
  background: #eef2f6;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #475569;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  text-transform: capitalize;
}


.badge.pending {
  background: #fff7ae;
  color: #854d0e;
}

.badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.badge.confirmed {
  background: #dbeafe;
  color: #1e3a8a;
}

.empty {
  padding: 18px;
  text-align: center;
  opacity: 0.7;
}
</style>
