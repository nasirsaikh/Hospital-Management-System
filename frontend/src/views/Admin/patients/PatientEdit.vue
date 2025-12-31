<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import patientAPI from "@/api/admin/patients";

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const patient = ref(null);
const loading = ref(true);

const loadPatient = async () => {
  try {
    const res = await patientAPI.getPatient(id);
    patient.value = res.data;
  } catch (e) {
    console.error("Failed to load patient:", e);
  }
  loading.value = false;
};

const save = async () => {
  try {
    const payload = {
      name: patient.value.user.name,
      email: patient.value.user.email,
      age: patient.value.age,
      gender: patient.value.gender,
      phone: patient.value.phone,
      address: patient.value.address
    };

    await patientAPI.updatePatient(id, payload);
    alert("Patient updated.");
    router.push("/admin/patients");
  } catch (e) {
    console.error("Update failed:", e);
    alert("Error while saving patient.");
  }
};

onMounted(loadPatient);
</script>

<template>
  <div class="page">


    <div class="header-card">
      <h1>Edit Patient</h1>
      <p>Modify patient details and update profile information.</p>
    </div>

    <div v-if="loading" class="loading-box">
      <div class="loader"></div>
      Loading patient...
    </div>

    <div v-else class="form-box">
      <form class="form">

        <div class="field">
          <label>Name</label>
          <input v-model="patient.user.name" />
        </div>

        <div class="field">
          <label>Email</label>
          <input v-model="patient.user.email" />
        </div>

        <div class="field">
          <label>Age</label>
          <input type="number" v-model.number="patient.age" />
        </div>

        <div class="field">
          <label>Gender</label>
          <select v-model="patient.gender">
            <option disabled value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <div class="field">
          <label>Phone</label>
          <input v-model="patient.phone" />
        </div>

        <div class="field">
          <label>Address</label>
          <textarea v-model="patient.address"></textarea>
        </div>

        <button class="btn-primary" @click.prevent="save">
          Save Changes
        </button>

      </form>
    </div>

  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 850px;
  margin: auto;
}


.header-card {
  background: linear-gradient(135deg, #1d3557, #457b9d);
  padding: 26px;
  border-radius: 14px;
  margin-bottom: 26px;
  color: white;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.header-card h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.header-card p {
  opacity: 0.9;
  margin-top: 4px;
}


.loading-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  color: #475569;
}

.loader {
  width: 22px;
  height: 22px;
  border: 4px solid #cbd5e1;
  border-top-color: #1d3557;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg)
  }
}


.form-box {
  background: white;
  padding: 28px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field label {
  font-weight: 600;
  margin-bottom: 4px;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}

textarea {
  resize: vertical;
}


.btn-primary {
  margin-top: 16px;
  background: #1d3557;
  color: white;
  padding: 12px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  width: 180px;
  transition: 0.2s;
}

.btn-primary:hover {
  background: #173049;
}
</style>
