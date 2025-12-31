<script setup>
import { ref } from "vue";
import specAPI from "@/api/admin/specializations";
import { useRouter } from "vue-router";
import { useToast } from "@/utils/useToast";

const toast = useToast();
const router = useRouter();

const name = ref("");
const description = ref("");

const save = async () => {
  await specAPI.create({
    name: name.value,
    description: description.value
  });

  toast.success("New department created");
  router.push("/admin/specializations");
};
</script>

<template>
  <div class="page">


    <div class="header-card">
      <h1>Create Department</h1>
      <p>Add a new medical department to the system.</p>
    </div>

    <div class="form-box">
      <form class="form">
        <div class="field">
          <label>Name</label>
          <input v-model="name" />
        </div>

        <div class="field">
          <label>Description</label>
          <textarea v-model="description"></textarea>
        </div>

        <button class="btn-primary" @click.prevent="save">
          Create Department
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
  font-size: 26px;
  font-weight: 700;
  margin: 0;
}

.header-card p {
  opacity: 0.9;
  margin-top: 4px;
}


.form-box {
  background: #fff;
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
  width: 200px;
  transition: 0.2s;
}

.btn-primary:hover {
  background: #172c45;
}
</style>
