<script setup>
import { ref, onMounted } from "vue";
import doctorAPI from "@/api/admin/doctors";

const doctors = ref([]);
const selectedDoctor = ref(null);
const slots = ref([]);
const newSlot = ref({ day: "", start: "", end: "" });

const loadDoctors = async () => {
  const res = await doctorAPI.getAll();
  doctors.value = res.data;
};

const loadAvailability = async () => {
  if (!selectedDoctor.value) return;
  const res = await doctorAPI.getAvailability(selectedDoctor.value);
  slots.value = res.data;
};

const addSlot = async () => {
  await doctorAPI.addAvailability(selectedDoctor.value, newSlot.value);
  newSlot.value = { day: "", start: "", end: "" };
  loadAvailability();
};

const deleteSlot = async (slotId) => {
  await doctorAPI.deleteAvailability(selectedDoctor.value, slotId);
  loadAvailability();
};

onMounted(loadDoctors);
</script>

<template>
  <div class="page">
    <h2>Doctor Availability Manager</h2>

    <div class="row">

      <select v-model="selectedDoctor" @change="loadAvailability">
        <option disabled value="">Select Doctor</option>
        <option v-for="d in doctors" :key="d.id" :value="d.id">
          {{ d.full_name }} — {{ d.specialization }}
        </option>
      </select>


      <div v-if="selectedDoctor" class="slot-form">
        <select v-model="newSlot.day">
          <option disabled value="">Day</option>
          <option>Monday</option>
          <option>Tuesday</option>
          <option>Wednesday</option>
          <option>Thursday</option>
          <option>Friday</option>
          <option>Saturday</option>
          <option>Sunday</option>
        </select>

        <input type="time" v-model="newSlot.start" />
        <input type="time" v-model="newSlot.end" />

        <button @click="addSlot">Add</button>
      </div>
    </div>


    <table v-if="slots.length" class="availability-table">
      <thead>
        <tr>
          <th>Day</th>
          <th>Start</th>
          <th>End</th>
          <th></th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="s in slots" :key="s.id">
          <td>{{ s.day }}</td>
          <td>{{ s.start }}</td>
          <td>{{ s.end }}</td>
          <td><button class="delete-btn" @click="deleteSlot(s.id)">X</button></td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<style scoped>
.page {
  padding: 20px;
}

.row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.availability-table {
  width: 100%;
  border-collapse: collapse;
}

.availability-table th,
.availability-table td {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.delete-btn {
  background: #ef4444;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
