<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import adminDoctorsAPI from "@/api/admin/doctors";
import DoctorForm from "./DoctorForm.vue";

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const form = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const res = await adminDoctorsAPI.get(id);
    form.value = res.data;
  } catch (e) {
    error.value = "Failed to load doctor details.";
    console.error(e);
  }
  loading.value = false;
});

const submit = async () => {
  try {
    await adminDoctorsAPI.update(id, form.value);
    router.push("/admin/doctors");
  } catch (e) {
    console.error(e);
    error.value = "Update failed.";
  }
};
</script>

<template>
  <div class="page">

    <div class="header-card">
      <h1>Edit Doctor</h1>
      <p>Modify the details below and save the updated profile.</p>
    </div>

    <div class="form-wrapper">

      <div v-if="loading" class="loading">Loading doctor data…</div>

      <div v-else-if="error" class="error-box">{{ error }}</div>

      <DoctorForm v-else :modelValue="form" @update:modelValue="form = $event" :editMode="true" :loading="false"
        @submit="submit" />
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

.loading {
  text-align: center;
  padding: 18px;
  font-size: 15px;
  opacity: 0.75;
}

.error-box {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #fecaca;
}
</style>
