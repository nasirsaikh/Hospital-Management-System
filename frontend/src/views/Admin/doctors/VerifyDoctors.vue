<script setup>
import { ref, computed, onMounted } from "vue";
import doctorAPI from "@/api/admin/doctors";
import { useRouter } from "vue-router";

const loading = ref(true);
const doctors = ref([]);
const filter = ref("ALL");

const fetchDoctors = async () => {
  loading.value = true;
  const res = await doctorAPI.getAll();
  doctors.value = res.data;
  loading.value = false;
};

onMounted(fetchDoctors);

const filtered = computed(() => {
  if (filter.value === "VERIFIED")
    return doctors.value.filter(d => d.is_verified);

  if (filter.value === "UNVERIFIED")
    return doctors.value.filter(d => !d.is_verified);

  return doctors.value;
});

const verifyDoctor = async (id) => {
  await doctorAPI.verify(id);
  fetchDoctors();
};
</script>

<template>
  <div class="page">
    <h2>Doctor Verification</h2>


    <div class="filters">
      <select v-model="filter">
        <option value="ALL">All</option>
        <option value="VERIFIED">Verified</option>
        <option value="UNVERIFIED">Unverified</option>
      </select>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <table v-else class="verification-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Specialization</th>
          <th>Verified?</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="d in filtered" :key="d.id">
          <td>{{ d.full_name }}</td>
          <td>{{ d.email }}</td>
          <td>{{ d.specialization }}</td>
          <td>
            <span :class="d.is_verified ? 'yes' : 'no'">
              {{ d.is_verified ? "Yes" : "No" }}
            </span>
          </td>
          <td>
            <button class="btn-verify" v-if="!d.is_verified" @click="verifyDoctor(d.id)">
              Verify
            </button>

            <span v-else class="verified-badge">✔ Verified</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.page {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

.verification-table {
  width: 100%;
  border-collapse: collapse;
}

.verification-table th,
.verification-table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.btn-verify {
  background: #1d3557;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.yes {
  color: #16a34a;
}

.no {
  color: #dc2626;
}

.verified-badge {
  color: #16a34a;
  font-weight: bold;
}
</style>
