<script setup>
import { ref, watch } from "vue";
import adminAPI from "@/api/admin/admin";
import { useToast } from "@/utils/useToast";

const props = defineProps({
  show: Boolean,
  patientId: Number,
});

const emit = defineEmits(["close"]);

const loading = ref(true);
const records = ref([]);
const toast = useToast();


watch(
  () => props.show,
  async (v) => {
    if (!v) return;

    loading.value = true;
    records.value = [];

    try {
      const res = await adminAPI.getPatientHistory(props.patientId);


      records.value = res.data.map((r, index) => ({
        ...structuredClone(r),
        open: false,
        uniqueKey: `${r.id}-${index}`,
      }));

    } catch (err) {
      console.error(err);
      toast.error("Failed to load patient medical history");
    }

    loading.value = false;
  }
);
</script>

<template>
  <div v-if="show" class="overlay">
    <div class="modal">


      <button class="close-btn" @click="$emit('close')">×</button>

      <h2 class="title">Patient Medical History</h2>


      <div v-if="loading" class="loading">Loading...</div>


      <div v-else-if="records.length === 0" class="empty">
        No medical history found.
      </div>


      <div v-else class="records-list">

        <div v-for="record in records" :key="record.uniqueKey" class="card">

          <div class="card-header">


            <div class="left">
              <div class="doctor">{{ record.doctor.name }}</div>
              <div class="spec">{{ record.doctor.specialization }}</div>
            </div>


            <div class="date">
              {{ record.date }} • {{ record.time }}
            </div>


            <button class="toggle" @click="record.open = !record.open">
              {{ record.open ? "Hide" : "View" }}
            </button>
          </div>


          <transition name="fade">
            <div v-if="record.open" class="details">

              <div class="row"><strong>Visit Type:</strong> {{ record.visit_type }}</div>
              <div class="row"><strong>Tests:</strong> {{ record.tests || "None" }}</div>
              <div class="row"><strong>Diagnosis:</strong> {{ record.diagnosis }}</div>
              <div class="row"><strong>Medicines:</strong> {{ record.medicines }}</div>
              <div class="row"><strong>Prescription:</strong> {{ record.prescription }}</div>
              <div class="row"><strong>Notes:</strong> {{ record.notes || "—" }}</div>

            </div>
          </transition>

        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
  backdrop-filter: blur(2px);
}


.modal {
  background: white;
  width: 650px;
  max-height: 85vh;
  overflow-y: auto;
  padding: 26px 30px;
  border-radius: 18px;
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.18);
  position: relative;
  animation: popup .25s ease;
}

@keyframes popup {
  from {
    transform: scale(.92);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}


.close-btn {
  position: absolute;
  right: 14px;
  top: 10px;
  font-size: 26px;
  background: none;
  border: none;
  color: #475569;
  cursor: pointer;
  opacity: .8;
}

.close-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}


.title {
  text-align: center;
  font-size: 22px;
  font-weight: 800;
  color: #13293d;
  margin-bottom: 18px;
}


.loading {
  text-align: center;
  padding: 20px 0;
  font-size: 15px;
  color: #475569;
}


.empty {
  text-align: center;
  padding: 24px;
  background: #f8fafc;
  border-radius: 12px;
  font-size: 15px;
  color: #6b7280;
}


.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}


.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  padding: 18px 20px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  transition: 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}


.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  flex-direction: column;
}

.doctor {
  font-size: 17px;
  font-weight: 700;
  color: #13293d;
}

.spec {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.date {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}


.toggle {
  padding: 6px 12px;
  background: #13293d;
  border-radius: 8px;
  color: white;
  border: none;
  cursor: pointer;
  transition: .18s;
}

.toggle:hover {
  opacity: .9;
}


.details {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #dbe4ea;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.row {
  font-size: 14px;
  color: #374151;
}

.row strong {
  color: #0f172a;
}


.fade-enter-active,
.fade-leave-active {
  transition: all .25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
