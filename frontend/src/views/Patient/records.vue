<script setup>
import { ref, onMounted } from "vue";
import recordsAPI from "@/api/patient/records";
import { useToast } from "@/utils/useToast";

const exporting = ref(false);

const startExport = async () => {
  if (exporting.value) return;

  exporting.value = true;

  try {
    await recordsAPI.startExport();
    toast.success("Export started. Check your email shortly.");
  } catch (e) {
    console.error(e);
    toast.error("Failed to start export");
  }

  setTimeout(() => {
    exporting.value = false;
  }, 1500); 
};

const loading = ref(true);
const records = ref([]);
const toast = useToast();

onMounted(async () => {
  try {
    const res = await recordsAPI.getAll();
    records.value = res.data.map(r => ({ ...r, open: false }));
  } catch (err) {
    console.error(err);
    toast.error("Failed to load medical records");
  }
  loading.value = false;
});
</script>


<template>
  <div class="page">

    <!-- Header -->
    <div class="header-block">
      <h1 class="title">My Medical Records</h1>
      <p class="subtitle">Your diagnoses, prescriptions, and past treatments.</p>
    </div>
    <button
  @click="startExport"
  class="export-btn"
  :disabled="exporting"
>
  <span v-if="!exporting">Export Treatments as CSV</span>
  <span v-else class="exporting-wrap">
    <span class="spinner"></span>
    Exporting…
  </span>
</button>



    <!-- Loader -->
    <div v-if="loading" class="loading-wrap">
      <div class="loader"></div>
      <p>Fetching your records...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="records.length === 0" class="empty">
      No medical records available.
    </div>

    <!-- Records List -->
    <div v-else class="records-list">

      <div v-for="record in records" :key="record.id" class="card">

        <!-- Top Row -->
        <div class="card-header">
          <div class="left">
            <div class="doctor">{{ record.doctor.name }}</div>
            <div class="spec">{{ record.doctor.specialization }}</div>
          </div>

          <div class="date">{{ record.date }}</div>

          <button class="toggle" @click="record.open = !record.open">
            {{ record.open ? "Hide" : "View" }}
          </button>
        </div>

        <!-- Expandable Content -->
        <transition name="fade">
          <div v-if="record.open" class="details">
            <div class="row"><strong>Visit Type:</strong> {{ record.visit_type }}</div>
            <div class="row"><strong>Tests Done:</strong> {{ record.tests || "None" }}</div>
            <div class="row"><strong>Diagnosis:</strong> {{ record.diagnosis }}</div>
            <div class="row"><strong>Medicines:</strong> {{ record.medicines }}</div>
            <div class="row"><strong>Prescription:</strong> {{ record.prescription }}</div>
            <div class="row"><strong>Notes:</strong> {{ record.notes || "—" }}</div>
          </div>
        </transition>

      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 850px;
  margin: auto;
}


.header-block {
  background: linear-gradient(135deg, #6ad4c4, #4ea8de);
  padding: 26px;
  border-radius: 18px;
  color: white;
  margin-bottom: 26px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
.title { font-size: 28px; font-weight: 800; }
.subtitle { opacity: 0.92; margin-top: 4px; font-size: 15px; }


.loading-wrap { text-align: center; padding-top: 40px; }
.loader {
  width: 28px; height: 28px;
  border: 3px solid #d1d5db;
  border-top-color: #4ea8de;
  border-radius: 50%; animation: spin 1s linear infinite;
  margin: auto;
}
@keyframes spin { to { transform: rotate(360deg); } }


.empty {
  text-align: center;
  padding: 40px;
  opacity: 0.7;
  font-size: 16px;
}


.records-list { display: flex; flex-direction: column; gap: 16px; }
.card {
  background: #fff;
  padding: 18px;
  border-radius: 16px;
  box-shadow: 0 3px 14px rgba(0,0,0,0.06);
  border: 1px solid #e6eef4;
}


.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.left { display: flex; flex-direction: column; }
.doctor { font-size: 18px; font-weight: 700; color: #265073; }
.spec { font-size: 13px; color: #6b7a8c; margin-top: -2px; }
.date { color: #4c566a; font-size: 14px; }

.toggle {
  padding: 6px 12px;
  background: #4ea8de;
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}


.details {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #dbe4ea;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.row { font-size: 14px; }


.fade-enter-active, .fade-leave-active {
  transition: all .25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0; transform: translateY(-6px);
}
.export-btn {
  margin-bottom: 22px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #4ea8de, #3a8ac4);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
  transition: transform 0.18s ease, box-shadow 0.18s ease, opacity .2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.export-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.18);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}


.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.5);
  border-top-color: white;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.exporting-wrap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}


</style>
