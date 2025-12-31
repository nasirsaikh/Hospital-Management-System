<script setup>
import { ref, onMounted } from "vue";
import PatientStatCard from "./components/PatientStatCard.vue";
import QuickActions from "./components/QuickActions.vue";
import UpcomingAppointmentCard from "./components/UpcomingAppointmentCard.vue";
import RecentAppointments from "./components/RecentAppointments.vue";
import RecentRecords from "./components/RecentRecords.vue";

import patientAPI from "@/api/patient/patient";
import { useAuthStore } from "@/store/auth";

const auth = useAuthStore();

const loading = ref(true);

const stats = ref({
  upcoming: 0,
  total: 0,
  completed: 0,
});

const upcomingAppointment = ref(null);
const recentAppointments = ref([]);
const recentRecords = ref([]);

onMounted(async () => {
  loading.value = true;

  try {
    const res = await patientAPI.dashboard();
    const data = res.data;

    stats.value = {
      upcoming: data.stats.upcoming,
      total: data.stats.total,
      completed: data.stats.completed,
    };

    upcomingAppointment.value = data.upcomingAppointment;
    recentAppointments.value = data.recentAppointments;
    recentRecords.value = data.recentRecords;

  } catch (err) {
    console.error("Dashboard error:", err);
  }

  loading.value = false;
});
</script>

<template>
  <div class="page">

    <!-- HEADER -->
    <div class="header-block">
      <h1 class="title">Welcome back, {{ auth.user?.name }} 👋</h1>
      <p class="subtitle">Your health overview at a glance</p>
    </div>

    <!-- STATS -->
    <section class="stats-grid">
      <PatientStatCard
        title="Upcoming"
        :value="stats.upcoming"
        description="Your next visits"
      />
      <PatientStatCard
        title="Total Bookings Made"
        :value="stats.total"
        description="Your lifetime appointments"
      />
      <PatientStatCard
        title="Completed"
        :value="stats.completed"
        description="Finished consultations"
      />
    </section>

    <!-- MAIN GRID -->
    <section class="main-grid">

      <div class="card">
        <UpcomingAppointmentCard
          :appointment="upcomingAppointment"
          :loading="loading"
        />
      </div>

      <div class="card">
        <QuickActions />
      </div>

    </section>

    <!-- Recent Appointments -->
    <div class="section-card">
      <RecentAppointments
        :items="recentAppointments"
        :loading="loading"
      />
    </div>

    <!-- Recent Records -->
    <div class="section-card">
      <RecentRecords
        :items="recentRecords"
        :loading="loading"
      />
    </div>

  </div>
</template>

<style scoped>

.page {
  padding: 26px;
  max-width: 1200px;
  margin: auto;
  
}


.header-block {
  background: linear-gradient(135deg, #66d1c6, #4ea8de);
  padding: 28px 32px;
  border-radius: 18px;
  color: white;
  margin-bottom: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.title {
  text-align: left;
  font-size: 28px;
  font-weight: 800;
}

.subtitle {
  margin-top: 4px;
  opacity: 0.92;
  font-size: 15px;
}


.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 20px;
  margin-top: 20px;
}


.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 26px;
  margin-top: 26px;
}

.card {
  background: white;
  padding: 22px;
  border-radius: 18px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.07);
  transition: transform 0.12s ease;
}

.card:hover {
  transform: translateY(-2px);
}


.section-card {
  background: white;
  padding: 22px;
  border-radius: 18px;
  margin-top: 28px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.06);
}

@media (max-width: 840px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}
</style>
