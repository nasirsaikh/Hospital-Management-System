<script setup>
import { ref, watch } from "vue";
import recordsAPI from "@/api/doctor/records";
import { useToast } from "@/utils/useToast";

const props = defineProps({
  show: Boolean,
  appointment: Object,
});

const emits = defineEmits(["close", "saved"]);

const toast = useToast();

const loading = ref(false);
const existingRecord = ref(null);

const form = ref({
  visit_type: "",
  tests: "",
  diagnosis: "",
  medicines: "",
  prescription: "",
  notes: "",
});


watch(
  () => props.show,
  async (open) => {
    if (!open) return;

    loading.value = true;
    existingRecord.value = null;


    form.value = {
      visit_type: "",
      tests: "",
      diagnosis: "",
      medicines: "",
      prescription: "",
      notes: "",
    };

    try {

      const res = await recordsAPI.getRecord(props.appointment.id);

      if (res.data && res.data.record) {
        existingRecord.value = res.data.record;


        form.value = {
          visit_type: res.data.record.visit_type || "",
          tests: res.data.record.tests || "",
          diagnosis: res.data.record.diagnosis || "",
          medicines: res.data.record.medicines || "",
          prescription: res.data.record.prescription || "",
          notes: res.data.record.notes || "",
        };
      }
    } catch (err) {
      console.warn("No existing record found");
    }

    loading.value = false;
  }
);


const saveRecord = async () => {
  try {
    const payload = {
      appointment_id: props.appointment.id,
      ...form.value,
    };

    await recordsAPI.save(payload);

    toast.success("Medical record saved successfully");

    emits("saved");
    emits("close");
  } catch (err) {
    console.error(err);
    toast.error("Failed to save record");
  }
};
</script>

<template>
  <div v-if="show" class="modal-bg">
    <div class="modal">

      <button class="close-btn" @click="$emit('close')">×</button>

      <h2 class="title">Patient Medical Record</h2>

      <div v-if="loading" class="loading">Loading record...</div>

      <div v-else class="form">

        <label>Visit Type</label>
        <input v-model="form.visit_type" placeholder="Clinic / Online / Emergency" />

        <label>Tests Done</label>
        <textarea v-model="form.tests" rows="2" placeholder="Blood Test, X-Ray, etc." />

        <label>Diagnosis</label>
        <textarea v-model="form.diagnosis" rows="2" placeholder="Diagnosis summary" />

        <label>Medicines</label>
        <textarea v-model="form.medicines" rows="2" placeholder="Medicine name, dosage" />

        <label>Prescription Instructions</label>
        <textarea v-model="form.prescription" rows="2" placeholder="Instructions for medicine intake" />

        <label>Additional Notes</label>
        <textarea v-model="form.notes" rows="2" placeholder="Optional doctor notes" />
      </div>

      <div class="footer">
        <button class="cancel" @click="$emit('close')">Cancel</button>
        <button class="save" @click="saveRecord">Save Record</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal {
  background: white;
  width: 520px;
  border-radius: 12px;
  padding: 22px 26px;
  position: relative;
  animation: pop 0.2s ease;
}

@keyframes pop {
  from {
    transform: scale(0.9);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 14px;
  font-size: 26px;
  background: none;
  border: none;
  cursor: pointer;
}

.title {
  font-size: 20px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 16px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input,
textarea {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 8px;
}

.loading {
  text-align: center;
  padding: 14px;
  opacity: 0.7;
}

.footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel {
  background: #e2e8f0;
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.save {
  background: #1d3557;
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}
</style>
