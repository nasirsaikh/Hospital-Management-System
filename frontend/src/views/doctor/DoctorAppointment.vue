<script setup>
import { ref, onMounted } from "vue";
import appointmentAPI from "@/api/doctor/appointments";
import { useToast } from "@/utils/useToast";

import ViewAppointmentModal from "./components/ViewAppointmentModal.vue";
import UpdateRecordModal from "./components/UpdateRecordModal.vue";
import PatientHistoryModal from "./components/PatientHistoryModal.vue";

const loading = ref(true);
const appointments = ref([]);

const showHistoryModal = ref(false);
const historyPatientId = ref(null);

const filters = ref({
  status: "",
  date_from: "",
  date_to: "",
});

const toast = useToast();


const showViewModal = ref(false);
const showRecordModal = ref(false);
const selectedAppointment = ref(null);


const load = async () => {
  loading.value = true;

  try {
    const res = await appointmentAPI.getAll({
      status: filters.value.status || undefined,
      date_from: filters.value.date_from || undefined,
      date_to: filters.value.date_to || undefined,
    });

    appointments.value = res.data;
  } catch (err) {
    console.error(err);
    toast.error("Failed to load appointments");
  }

  loading.value = false;
};

const resetFilters = () => {
  filters.value = { status: "", date_from: "", date_to: "" };
  load();
};


const openViewModal = (appt) => {
  selectedAppointment.value = appt;
  showViewModal.value = true;
};

const openRecordModal = (appt) => {
  selectedAppointment.value = appt;
  showRecordModal.value = true;
};

const openHistoryModal = (appt) => {
  historyPatientId.value = appt.patient.id;
  showHistoryModal.value = true;
};


const markComplete = async (appt) => {
  try {
    await appointmentAPI.markComplete(appt.id);
    toast.success("Appointment marked completed");
    load();
  } catch (err) {
    toast.error("Failed to update appointment");
  }
};

onMounted(load);
</script>

<template>
  <div class="page">


    <div class="header">
      <h1>Appointments</h1>
    </div>


    <div class="filters">
      <select v-model="filters.status" @change="load">
        <option value="">All Statuses</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>

      <input type="date" v-model="filters.date_from" @change="load" />
      <input type="date" v-model="filters.date_to" @change="load" />

      <button class="reset" @click="resetFilters">Reset</button>
    </div>


    <div v-if="loading" class="loading">
      <div class="loader"></div>
      Fetching appointments...
    </div>


    <div v-else-if="appointments.length === 0" class="empty">
      No appointments found.
    </div>


    <div v-else class="list">

      <div v-for="a in appointments" :key="a.id" class="card">

        <div class="left">
          <div class="patient-name">{{ a.patient.name }}</div>
          <div class="meta">
            {{ a.patient.age }} yrs • {{ a.patient.gender }}
          </div>
        </div>


        <div class="mid">
          <div class="date">{{ a.date }}</div>
          <div class="time">{{ a.time }}</div>
        </div>


        <div class="status" :class="a.status">
          {{ a.status }}
        </div>


        <div class="actions">
          <button class="view" @click="openViewModal(a)">View</button>
          <button class="history" @click="openHistoryModal(a)">History</button>

          <button v-if="a.status === 'pending'" class="update" @click="openRecordModal(a)">Record</button>
          <button v-if="a.status === 'pending'" class="done" @click="markComplete(a)">Complete</button>
        </div>
      </div>

    </div>


    <ViewAppointmentModal :show="showViewModal" :appointment="selectedAppointment" @close="showViewModal = false" />

    <UpdateRecordModal :show="showRecordModal" :appointment="selectedAppointment" @close="showRecordModal = false"
      @saved="load" />

    <PatientHistoryModal :show="showHistoryModal" :patient-id="historyPatientId" @close="showHistoryModal = false" />

  </div>
</template>

<style scoped>
.page {
  padding: 28px;
  max-width: 1100px;
  margin: auto;
}


.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #13293d;
  margin-bottom: 18px;
}


.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 22px;
}

.filters select,
.filters input {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 14px;
  background: #f9fafb;
}

.reset {
  padding: 10px 14px;
  background: #dc2626;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  border: none;
}


.loading {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #4b5563;
}

.loader {
  width: 26px;
  height: 26px;
  border: 4px solid #cbd5e1;
  border-top-color: #13293d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.empty {
  text-align: center;
  padding: 20px;
  font-size: 15px;
  opacity: 0.7;
}


.list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}


.card {
  background: white;
  padding: 18px 20px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  display: grid;
  grid-template-columns: 1.4fr 1fr 120px auto;
  align-items: center;
  border: 1px solid #e5e7eb;
}


.patient-name {
  font-size: 18px;
  font-weight: 700;
  color: #13293d;
}

.meta {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}


.date {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

.time {
  color: #6b7280;
}


.status {
  padding: 6px 12px;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  text-transform: capitalize;
  font-size: 14px;
}

.status.pending {
  background: #fff7d6;
  color: #854d0e;
}

.status.completed {
  background: #dbeafe;
  color: #1e40af;
}

.status.cancelled {
  background: #fee2e2;
  color: #b91c1c;
}


.actions {
  margin-left: 10px;
  display: flex;
  gap: 8px;
}

.actions button {
  padding: 7px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  min-width: 80px;
  color: white;
}

.actions .view {
  background: #13293d;
}

.actions .history {
  background: #475569;
}

.actions .update {
  background: #0ea5e9;
}

.actions .done {
  background: #16a34a;
}

.actions button:hover {
  opacity: 0.9;
}


@media (max-width: 900px) {
  .card {
    grid-template-columns: 1fr 1fr;
    grid-row-gap: 12px;
  }

  .mid,
  .status {
    justify-self: start;
  }

  .actions {
    grid-column: span 2;
    justify-content: flex-start;
  }
}
</style>
