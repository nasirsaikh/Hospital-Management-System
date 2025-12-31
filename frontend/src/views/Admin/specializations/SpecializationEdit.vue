<script setup>
import { ref, onMounted } from "vue";
import specAPI from "@/api/admin/specializations";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "@/utils/useToast";

const toast = useToast();

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const spec = ref({
  name: "",
  description: ""
});

const loading = ref(true);

const load = async () => {
  try {
    const res = await specAPI.getAll();
    spec.value = res.data.find((s) => s.id == id);
  } catch (err) {
    console.error(err);
  }
  loading.value = false;
};

const save = async () => {
  await specAPI.update(id, spec.value);
  toast.success("Department updated successfully");
  router.push("/admin/specializations");
};

onMounted(load);
</script>

<template>
  <div class="page">


    <div class="header-card">
      <h1>Edit Department</h1>
      <p>Modify the details of this department.</p>
    </div>

    <div v-if="loading" class="loading-box">
      <div class="loader"></div>
      Loading department…
    </div>

    <div v-else class="form-box">
      <form class="form">
        <div class="field">
          <label>Name</label>
          <input v-model="spec.name" />
        </div>

        <div class="field">
          <label>Description</label>
          <textarea v-model="spec.description"></textarea>
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
  max-width: 800px;
  margin: auto;
}


.header-card {
  background: linear-gradient(135deg, #1d3557, #457b9d);
  padding: 24px 28px;
  color: white;
  border-radius: 14px;
  margin-bottom: 26px;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.15);
}

.header-card h1 {
  margin: 0;
  font-size: 26px;
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
  color: #475569;
  padding: 16px;
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
    transform: rotate(360deg);
  }
}


.form-box {
  background: #ffffff;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.08);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field label {
  font-weight: 600;
  margin-bottom: 4px;
  display: block;
}

.field input,
.field textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
}

textarea {
  resize: vertical;
}


.btn-primary {
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
  background: #172c45;
}
</style>
