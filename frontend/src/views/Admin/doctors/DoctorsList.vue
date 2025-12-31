<script setup>
import { ref, computed, onMounted } from "vue";
import adminDoctorsAPI from "@/api/admin/doctors";
import { useRouter } from "vue-router";

const router = useRouter();

const loading = ref(true);
const doctors = ref([]);
const search = ref("");

const showModal = ref(false);
const selectedDoctor = ref(null);

const load = async () => {
  loading.value = true;
  try {
    const res = await adminDoctorsAPI.getAll();
    doctors.value = res.data || [];
  } catch (err) {
    console.error(err);
  }
  loading.value = false;
};

onMounted(load);


const filtered = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return doctors.value;

  return doctors.value.filter((d) => {
    return (
      (d.full_name || "").toLowerCase().includes(q) ||
      (d.email || "").toLowerCase().includes(q) ||
      (d.specialization || "").toLowerCase().includes(q)
    );
  });
});


const toggleStatus = async (id) => {
  try {
    await adminDoctorsAPI.toggleStatus(id);
    load();
  } catch (err) {
    console.error(err);
  }
};


const verifyDoctor = async () => {
  try {
    await adminDoctorsAPI.verify(selectedDoctor.value.id);
    showModal.value = false;
    load();
  } catch (err) {
    console.error(err);
  }
};

const openVerifyModal = (doc) => {
  selectedDoctor.value = doc;
  showModal.value = true;
};
</script>

<template>
  <div class="page">


    <div class="header">
      <h1>Doctors Management</h1>
      <button class="btn add-btn" @click="router.push('/admin/doctors/add')">
        + Add Doctor
      </button>
    </div>


    <div class="search-box">
      <i class="fa fa-search search-icon"></i>
      <input v-model="search" placeholder="Search doctors..." class="search-input" />
    </div>


    <div v-if="loading" class="loading">Loading doctors...</div>
    <div v-else-if="filtered.length === 0" class="empty">No doctors found.</div>


    <div v-else class="table-card">
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Specialization</th>
            <th>Experience</th>
            <th>Status</th>
            <th>Verification</th>
            <th style="width:160px">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="d in filtered" :key="d.id">
            <td>{{ d.full_name }}</td>
            <td>{{ d.email }}</td>
            <td>{{ d.specialization }}</td>
            <td>{{ d.experience_years }} yrs</td>


            <td>
              <span class="badge status" :class="d.is_active ? 'active' : 'inactive'" @click="toggleStatus(d.id)">
                {{ d.is_active ? "Active" : "Inactive" }}
              </span>
            </td>


            <td>
              <span v-if="d.is_verified" class="badge verified">Verified</span>

              <button v-else class="btn verify-btn" @click="openVerifyModal(d)">
                Verify
              </button>
            </td>


            <td>
              <button class="btn edit-btn" @click="router.push(`/admin/doctors/edit/${d.id}`)">
                Edit
              </button>
            </td>
          </tr>
        </tbody>

      </table>
    </div>


    <div v-if="showModal" class="modal-backdrop">
      <div class="modal">
        <h3 class="modal-title">Verify Doctor</h3>

        <div class="modal-content">
          <p><strong>Name:</strong> {{ selectedDoctor.full_name }}</p>
          <p><strong>Email:</strong> {{ selectedDoctor.email }}</p>
          <p><strong>Phone:</strong> {{ selectedDoctor.phone || "N/A" }}</p>
        </div>

        <div class="modal-actions">
          <button class="btn confirm-btn" @click="verifyDoctor">Verify Doctor</button>
          <button class="btn close-btn" @click="showModal = false">Close</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.page {
  padding: 28px;
  max-width: 1250px;
  margin: auto;
}


.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1d3557;
}

.add-btn {
  background: #1d3557;
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
}

.btn {
  border: none;
  cursor: pointer;
}


.search-box {
  position: relative;
  margin-bottom: 20px;
  width: 360px;
}

.search-icon {
  position: absolute;
  top: 11px;
  left: 12px;
  color: #64748b;
}

.search-input {
  padding: 10px 14px 10px 36px;
  width: 100%;
  border-radius: 8px;
  border: 1px solid #cdd5e0;
  background: white;
}


.loading,
.empty {
  padding: 20px;
  text-align: center;
  color: #6b7280;
}


.table-card {
  background: white;
  padding: 0;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  background: #eef2f6;
  padding: 14px;
  text-align: left;
  font-weight: 600;
  color: #455a75;
}

.table td {
  padding: 14px;
  border-bottom: 1px solid #e5e7eb;
}

.table tr:hover {
  background-color: #f8fafc;
}


.badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  cursor: pointer;
}

.badge.status.active {
  background: #d1fae5;
  color: #065f46;
}

.badge.status.inactive {
  background: #fee2e2;
  color: #b91c1c;
}

.badge.verified {
  background: #d1fae5;
  color: #166534;
}


.verify-btn {
  background: #457b9d;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
}

.edit-btn {
  background: #1d3557;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
}


.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal {
  background: white;
  width: 360px;
  padding: 22px 26px;
  border-radius: 12px;
  animation: fadeIn 0.2s ease-out;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-title {
  font-size: 20px;
  margin-bottom: 12px;
  color: #1d3557;
}

.modal-content p {
  margin: 6px 0;
  color: #334155;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 18px;
}

.confirm-btn {
  background: #22c55e;
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
}

.close-btn {
  background: #e2e8f0;
  padding: 8px 14px;
  border-radius: 6px;
}
</style>
