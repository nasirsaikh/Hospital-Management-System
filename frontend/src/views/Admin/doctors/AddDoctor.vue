<script setup>
import { ref } from "vue";
import adminDoctorsAPI from "@/api/admin/doctors";
import { useRouter } from "vue-router";
import DoctorForm from "./DoctorForm.vue";

const router = useRouter();

const form = ref({
  full_name: "",
  email: "",
  phone: "",
  gender: "",
  age: null,
  specialization_id: null,
  qualification: "",
  experience_years: null,
  consultation_fee: null,
  password: "",
  bio: ""
});

const loading = ref(false);
const error = ref("");

const submit = async () => {
  if (loading.value) return;
  loading.value = true;
  error.value = "";

  try {
    const payload = Object.fromEntries(
      Object.entries(form.value).filter(([_, v]) => v !== "" && v !== null)
    );

    await adminDoctorsAPI.create(payload);
    router.push("/admin/doctors");

  } catch (e) {
    console.error("Create doctor failed:", e);
    error.value =
      e?.response?.data?.message || e?.message || "Failed to create doctor";

  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="page">

    <div class="header-card">
      <h1>Add New Doctor</h1>
      <p>Fill in the information below to register a new doctor.</p>
    </div>

    <div class="form-wrapper">

      <div v-if="error" class="error-box">
        {{ error }}
      </div>

      <DoctorForm v-model="form" :editMode="false" :loading="loading" @submit="submit" />
    </div>

  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 920px;
  margin: auto;
}


.header-card {
  background: linear-gradient(135deg, #1d3557, #457b9d);
  padding: 24px 28px;
  border-radius: 14px;
  color: white;
  margin-bottom: 26px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.header-card h1 {
  font-size: 26px;
  margin: 0;
  font-weight: 700;
}

.header-card p {
  margin-top: 6px;
  opacity: 0.9;
}


.form-wrapper {
  background: white;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.error-box {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #fecaca;
}
</style>
