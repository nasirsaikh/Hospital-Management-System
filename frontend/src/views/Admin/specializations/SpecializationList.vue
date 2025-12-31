<script setup>
import { ref, onMounted, computed } from "vue";
import specAPI from "@/api/admin/specializations";
import { useRouter } from "vue-router";

const router = useRouter();

const specializations = ref([]);
const loading = ref(true);
const search = ref("");


const loadSpecs = async () => {
  loading.value = true;
  try {
    const res = await specAPI.getAll();
    specializations.value = res.data;
  } catch (err) {
    console.error(err);
  }
  loading.value = false;
};


const filteredSpecs = computed(() => {
  const term = search.value.toLowerCase().trim();

  if (!term) return specializations.value;

  return specializations.value.filter((s) =>
    s.name.toLowerCase().includes(term) ||
    (s.description || "").toLowerCase().includes(term)
  );
});


const addNew = () => {
  router.push("/admin/specializations/create");
};

const editSpec = (id) => {
  router.push(`/admin/specializations/${id}/edit`);
};

const deleteSpec = async (id) => {
  if (confirm("Are you sure you want to delete this department?")) {
    await specAPI.delete(id);
    loadSpecs();
  }
};

onMounted(loadSpecs);
</script>

<template>
  <div class="page">


    <div class="header-card">
      <h1>Departments</h1>
      <p>Manage all hospital departments and their descriptions.</p>
    </div>


    <div class="top-bar">
      <input type="text" v-model="search" placeholder="Search departments..." class="search-input" />

      <button class="btn-primary" @click="addNew">+ Add Department</button>
    </div>


    <div v-if="loading" class="loading-box">
      <div class="loader"></div>
      Loading departments…
    </div>


    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Department Name</th>
            <th>Description</th>
            <th class="right">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="s in filteredSpecs" :key="s.id">
            <td>{{ s.name }}</td>
            <td>{{ s.description || '—' }}</td>

            <td class="right actions">
              <button class="btn-edit" @click="editSpec(s.id)">Edit</button>
              <button class="btn-delete" @click="deleteSpec(s.id)">Delete</button>
            </td>
          </tr>


          <tr v-if="filteredSpecs.length === 0">
            <td colspan="3" class="empty-row">
              No matching departments found.
            </td>
          </tr>

        </tbody>
      </table>
    </div>

  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 1100px;
  margin: auto;
}


.header-card {
  background: linear-gradient(135deg, #1d3557, #457b9d);
  padding: 24px 28px;
  border-radius: 14px;
  color: #fff;
  margin-bottom: 26px;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.15);
}

.header-card h1 {
  font-size: 26px;
  margin: 0;
  font-weight: 700;
}


.top-bar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.search-input {
  flex: 1;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: white;
  font-size: 14px;
  transition: 0.2s;
}

.search-input:focus {
  border-color: #457b9d;
  box-shadow: 0 0 8px rgba(69, 123, 157, 0.4);
  outline: none;
}

.btn-primary {
  background: #1d3557;
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn-primary:hover {
  background: #162b45;
}


.loading-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  color: #475569;
}

.loader {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 4px solid #cbd5e1;
  border-top-color: #1d3557;
  animation: spin 1s linear infinite;
}


.table-wrapper {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0px 4px 18px rgba(0, 0, 0, 0.08);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f1f5f9;
}

.data-table th,
.data-table td {
  padding: 14px 16px;
}

.data-table td {
  border-bottom: 1px solid #e2e8f0;
  color: #334155;
}


.empty-row {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
}


.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-edit,
.btn-delete {
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  font-size: 13px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-edit {
  background: #457b9d;
  color: white;
}

.btn-edit:hover {
  background: #3a6680;
}

.btn-delete {
  background: #e63946;
  color: white;
}

.btn-delete:hover {
  background: #c62832;
}
</style>
