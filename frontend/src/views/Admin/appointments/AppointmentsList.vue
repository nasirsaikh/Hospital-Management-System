<script setup>
import { ref, computed, onMounted } from "vue";
import adminAPI from "@/api/admin/admin";
import doctorRecordsAPI from "@/api/doctor/records";
import { useToast } from "@/utils/useToast";

import AdminViewModal from "@/views/doctor/components/ViewAppointmentModal.vue";
import PatientHistoryModal from "../components/PatientHistoryModal.vue";

const toast = useToast();

const loading = ref(true);
const appointments = ref([]);

const search = ref("");
const statusFilter = ref("ALL");


const showViewModal = ref(false);
const showHistoryModal = ref(false);

const selectedAppointment = ref(null);
const historyPatientId = ref(null);

const load = async () => {
  loading.value = true;
  try {
    const res = await adminAPI.getAppointments();
    appointments.value = res.data;
  } catch (err) {
    console.error(err);
    toast.error("Failed to load appointments");
  }
  loading.value = false;
};

onMounted(load);

const filtered = computed(() => {
  let rows = [...appointments.value];

  if (statusFilter.value !== "ALL") {
    rows = rows.filter(a => a.status === statusFilter.value.toLowerCase());
  }

  if (search.value.trim()) {
    const q = search.value.toLowerCase();
    rows = rows.filter(a =>
      a.doctor?.name?.toLowerCase().includes(q) ||
      a.patient?.name?.toLowerCase().includes(q) ||
      a.date.includes(q)
    );
  }

  return rows;
});


const updateStatus = async (id, status) => {
  try {
    await adminAPI.updateAppointmentStatus(id, { status });
    toast.success("Status updated");
    load();
  } catch (err) {
    console.error(err);
    toast.error("Update failed");
  }
};


const openViewModal = (appt) => {
  selectedAppointment.value = appt;
  showViewModal.value = true;
};


const openHistory = (appt) => {
  historyPatientId.value = appt.patient.id;
  showHistoryModal.value = true;
};
</script>

<template>
  <div class="page">
    
    <div class="header">
      <h1>Manage Appointments</h1>
      <p class="sub">Monitor and manage all hospital appointments</p>
    </div>

    
    <div class="card filter-card">
      <input
        v-model="search"
        class="input"
        placeholder="Search by doctor, patient or date..."
      />

      <select v-model="statusFilter" class="input">
        <option value="ALL">All Status</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    
    <div v-if="loading" class="loading-box">
      <div class="loader"></div>
      <span>Loading appointments...</span>
    </div>

    
    <div v-else class="card table-card">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Doctor</th>
            <th>Patient</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th style="width: 260px; text-align:right;">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="a in filtered" :key="a.id">
            <td>{{ a.id }}</td>
            <td>{{ a.doctor?.name || '-' }}</td>
            <td>{{ a.patient?.name || '-' }}</td>
            <td>{{ a.date }}</td>
            <td>{{ a.time }}</td>

            <td>
              <span class="badge" :class="a.status">
                {{ a.status }}
              </span>
            </td>

            <td class="actions">
              <div class="btn-group">

                
                <button class="btn btn-view" @click="openViewModal(a)">
                  View
                </button>

                
                <button class="btn btn-history" @click="openHistory(a)">
                  History
                </button>

                
                <button
                  v-if="a.status === 'pending'"
                  class="btn btn-complete"
                  @click="updateStatus(a.id, 'completed')"
                >
                  Complete
                </button>

                
                <button
                  v-if="a.status === 'pending'"
                  class="btn btn-cancel"
                  @click="updateStatus(a.id, 'cancelled')"
                >
                  Cancel
                </button>
                
                <button
                  v-if="a.status === 'completed'"
                  class="btn btn-pending"
                  @click="updateStatus(a.id, 'pending')"
                >
                  Mark Pending
                </button>

              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    
    <AdminViewModal
      :show="showViewModal"
      :appointment="selectedAppointment"
      @close="showViewModal = false"
    />

    
    <PatientHistoryModal
      :show="showHistoryModal"
      :patient-id="historyPatientId"
      @close="showHistoryModal = false"
    />

  </div>
</template>

<style scoped>

.page {
  padding: 28px;
  max-width: 1200px;
  margin: auto;
}
.header {
  margin-bottom: 22px;
}
.header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1d3557;
}
.sub {
  color: #64748b;
  margin-top: 4px;
}


.card {
  background: white;
  padding: 18px;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  margin-bottom: 20px;
}


.filter-card {
  display: flex;
  gap: 14px;
}
.input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px;
  font-size: 14px;
  flex: 1;
}


.table-card {
  padding: 0;
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}
.table thead {
  background: #f1f5f9;
}
.table th,
.table td {
  padding: 14px;
  border-bottom: 1px solid #e2e8f0;
}
.table tr:hover {
  background: #f8fafc;
}


.badge {
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: capitalize;
  font-size: 12px;
  font-weight: 600;
}
.badge.pending { background: #fff7d6; color: #854d0e; }
.badge.confirmed { background: #d1fae5; color: #065f46; }
.badge.completed { background: #dbeafe; color: #1e3a8a; }
.badge.cancelled { background: #fee2e2; color: #b91c1c; }


.actions {
  text-align: right;
}

.btn-group {
  display: inline-flex;
  gap: 8px;
}

.btn {
  padding: 7px 14px;
  border-radius: 8px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: white;
  transition: 0.15s ease;
  min-width: 90px;
  text-align: center;
}

.btn-view    { background: #1d3557; }
.btn-history { background: #457b9d; }
.btn-complete { background: #16a34a; }
.btn-cancel  { background: #dc2626; }
.btn-pending  { background: #854d0e; }


.btn-view:hover { background: #162b45; }
.btn-history:hover { background: #3a6680; }
.btn-complete:hover { background: #15803d; }
.btn-cancel:hover { background: #b91c1c; }


.loading-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px;
}
.loader {
  width: 22px;
  height: 22px;
  border: 3px solid #cbd5e1;
  border-top-color: #1d3557;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
