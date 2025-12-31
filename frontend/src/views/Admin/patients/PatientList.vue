<script setup>
import { ref, onMounted, computed } from "vue";
import patientAPI from "@/api/admin/patients";
import { useRouter } from "vue-router";

const patients = ref([]);
const loading = ref(true);
const search = ref("");
const router = useRouter();


const loadPatients = async () => {
  loading.value = true;
  try {
    const res = await patientAPI.getAllPatients();
    patients.value = res.data || [];
  } catch (e) {
    console.error("Failed to load patients:", e);
  }
  loading.value = false;
};


const filteredPatients = computed(() => {
  const term = search.value.toLowerCase().trim();

  if (!term) return patients.value;

  return patients.value.filter((p) =>
    (p.user?.name || "").toLowerCase().includes(term) ||
    (p.user?.email || "").toLowerCase().includes(term) ||
    (p.phone || "").toLowerCase().includes(term)
  );
});


const editPatient = (id) => {
  router.push(`/admin/patients/${id}/edit`);
};

const toggleStatus = async (id) => {
  try {
    await patientAPI.togglePatientStatus(id);
    loadPatients();
  } catch (e) {
    console.error("Status toggle failed:", e);
  }
};

const deletePatient = async (id) => {
  if (confirm("Delete this patient? This cannot be undone.")) {
    try {
      await patientAPI.deletePatient(id);
      loadPatients();
    } catch (e) {
      console.error("Failed to delete:", e);
    }
  }
};

onMounted(loadPatients);
</script>

<template>
  <div class="page">


    <div class="header-card">
      <h1>Patients Management</h1>
      <p>Manage all registered patients in the system.</p>
    </div>


    <div class="top-bar">
      <input v-model="search" type="text" class="search-input"
        placeholder="Search patients by name, email or phone..." />
    </div>


    <div v-if="loading" class="loading-box">
      <div class="loader"></div>
      Loading patients…
    </div>


    <table v-else class="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Age</th>
          <th>Gender</th>
          <th>Phone</th>
          <th>Status</th>
          <th style="text-align:right;">Actions</th>
        </tr>
      </thead>

      <tbody>


        <tr v-if="filteredPatients.length === 0">
          <td colspan="7" class="empty-row">No matching patients found.</td>
        </tr>


        <tr v-for="p in filteredPatients" :key="p.id">
          <td>{{ p.user?.name || "-" }}</td>
          <td>{{ p.user?.email || "-" }}</td>
          <td>{{ p.age || "-" }}</td>
          <td>{{ p.gender || "-" }}</td>
          <td>{{ p.phone || "-" }}</td>

          <td>
            <span :class="p.user?.is_active ? 'tag-active' : 'tag-inactive'">
              {{ p.user?.is_active ? "Active" : "Inactive" }}
            </span>
          </td>

          <td class="actions">
            <button class="btn-edit" @click="editPatient(p.id)">Edit</button>

            <button :class="p.user?.is_active ? 'btn-disable' : 'btn-enable'" @click="toggleStatus(p.id)">
              {{ p.user?.is_active ? "Disable" : "Enable" }}
            </button>

            <button class="btn-delete" @click="deletePatient(p.id)">Delete</button>
          </td>
        </tr>

      </tbody>
    </table>

  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 1200px;
  margin: auto;
}


.header-card {
  background: linear-gradient(135deg, #1d3557, #457b9d);
  padding: 26px;
  border-radius: 14px;
  margin-bottom: 24px;
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


.top-bar {
  display: flex;
  margin-bottom: 16px;
}


.search-input {
  flex: 1;
  padding: 12px 14px;
  font-size: 14px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: white;
  transition: 0.2s ease;
}

.search-input:focus {
  border-color: #457b9d;
  box-shadow: 0 0 8px rgba(69, 123, 157, 0.4);
  outline: none;
}


.loading-box {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  color: #475569;
  padding: 12px;
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
    transform: rotate(360deg)
  }
}


.data-table {
  width: 100%;
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  border-collapse: collapse;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.data-table th {
  background: #f1f5f9;
  color: #1e293b;
  padding: 14px;
  font-size: 14px;
}

.data-table td {
  padding: 14px;
  border-bottom: 1px solid #e2e8f0;
}

.empty-row {
  text-align: center;
  padding: 16px;
  color: #6b7280;
  font-style: italic;
}


.tag-active {
  padding: 6px 10px;
  background: #dcfce7;
  color: #166534;
  border-radius: 6px;
  font-size: 13px;
}

.tag-inactive {
  padding: 6px 10px;
  background: #fee2e2;
  color: #b91c1c;
  border-radius: 6px;
  font-size: 13px;
}


.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn-edit {
  background: #457b9d;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
}

.btn-enable {
  background: #22c55e;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
}

.btn-disable {
  background: #f59e0b;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
}

.btn-delete {
  background: #e63946;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
}
</style>
