<script setup>
import { ref, onMounted, computed } from "vue";
import AppointmentCard from "./components/AppointmentCard.vue";
import AppointmentFilters from "./components/AppointmentFilters.vue";
import CancelConfirmModal from "./components/CancelConfirmModal.vue";

import appointmentAPI from "@/api/patient/appointments";
import { useToast } from "@/utils/useToast";


const toast = useToast?.() ?? {
  success: (m) => alert(m),
  error: (m) => alert(m),
};

const loading = ref(true);
const appointments = ref([]);

const filter = ref("all");

const showCancelModal = ref(false);
const selectedAppointment = ref(null);


const load = async () => {
  loading.value = true;

  try {
    const res = await appointmentAPI.getAll();
    appointments.value =
      res?.data?.appointments ?? res?.appointments ?? [];
  } catch (e) {
    toast.error("Failed to load appointments");
  }

  loading.value = false;
};


const filteredAppointments = computed(() => {
  if (filter.value === "all") return appointments.value;
  return appointments.value.filter((a) => a.status === filter.value);
});


const openCancelModal = (appt) => {
  selectedAppointment.value = appt;
  showCancelModal.value = true;
};

const cancelAppointment = async () => {
  try {
    await appointmentAPI.cancel(selectedAppointment.value.id);
    toast.success("Appointment cancelled");
    showCancelModal.value = false;
    await load();
  } catch {
    toast.error("Could not cancel appointment");
  }
};

onMounted(load);
</script>

<template>
  <div class="page">

    <!-- HEADER -->
    <div class="header-block">
      <h1 class="title">My Appointments</h1>
      <p class="subtitle">View, manage and cancel your appointments</p>
    </div>

    <!-- FILTERS -->
    <div class="filters-wrapper">
      <AppointmentFilters v-model="filter" />
    </div>

    <!-- LIST / EMPTY / LOADING -->
    <div v-if="loading" class="loading">Loading your appointments...</div>

    <div v-else>
      <p v-if="filteredAppointments.length === 0" class="empty">
        You have no appointments in this category.
      </p>

      <div class="list" v-else>
        <AppointmentCard
          v-for="a in filteredAppointments"
          :key="a.id"
          :appointment="a"
          @cancel="openCancelModal"
        />
      </div>
    </div>

    <!-- CANCEL MODAL -->
    <CancelConfirmModal
      :show="showCancelModal"
      :appointment="selectedAppointment"
      @confirm="cancelAppointment"
      @close="showCancelModal = false"
    />
  </div>
</template>

<style scoped>

.page {
  padding: 26px;
  max-width: 900px;
  margin: auto;
  
}


.header-block {
  background: linear-gradient(135deg, #6ad4c4, #4ea8de);
  padding: 24px 28px;
  border-radius: 16px;
  color: white;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  margin-bottom: 26px;
}

.title {
  font-size: 26px;
  font-weight: 800;
}

.subtitle {
  opacity: 0.92;
  margin-top: 4px;
}


.filters-wrapper {
  background: white;
  padding: 14px 18px;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  margin-bottom: 20px;
}


.list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}


.empty {
  text-align: center;
  padding: 34px;
  font-size: 16px;
  opacity: 0.7;
}


.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #7b8a97;
}
</style>
