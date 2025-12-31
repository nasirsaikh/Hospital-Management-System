<script setup>
import { ref, onMounted } from "vue";
import doctorAPI from "@/api/patient/doctors";
import appointmentAPI from "@/api/patient/appointments";
import specializations from "@/api/admin/specializations"; 
import { useToast } from "@/utils/useToast";

import DoctorCard from "./components/DoctorCard.vue";
import DoctorDetailsModal from "./components/DoctorDetailsModal.vue";
import SlotBookingModal from "./components/SlotBookingModal.vue";

const { success, error } = useToast();


const doctors = ref([]);
const loading = ref(true);


const search = ref("");
const specialization = ref("");
const sort = ref("");


const specializationss = ref([]);


const selectedDoctor = ref(null);
const showDetails = ref(false);
const showSlots = ref(false);
const availableSlots = ref([]);


const loadSpecializations = async () => {
  try {
    const res = await specializations.getAll();
    specializationss.value = res.data;
  } catch (e) {
    console.error(e);
    error("Failed to load specializations");
  }
};


const loadDoctors = async () => {
  loading.value = true;
  try {
    const res = await doctorAPI.getAllDoctors({
      search: search.value,
      specialization: specialization.value,
      sort: sort.value,
    });
    doctors.value = res.data;
  } catch (e) {
    error("Failed to load doctors");
  }
  loading.value = false;
};

onMounted(async () => {
  await loadSpecializations();
  await loadDoctors();
});


const openDetails = async (doctor) => {
  const res = await doctorAPI.getDoctorProfile(doctor.id);
  selectedDoctor.value = res.data;
  showDetails.value = true;
};


const openBooking = async (doctor) => {
  selectedDoctor.value = doctor;
  const res = await doctorAPI.getAvailability(doctor.id);
  availableSlots.value = res.data;
  showSlots.value = true;
};


const bookSlot = async (slot) => {
  try {
    await appointmentAPI.book({
      doctor_id: selectedDoctor.value.id,
      date: slot.date,
      time: slot.time,
    });
    success("Appointment booked!");
    showSlots.value = false;
  } catch {
    error("Failed to book appointment");
  }
};
</script>

<template>
  <div class="page">

    <!-- Header -->
    <div class="header-block">
      <h1 class="title">Book an Appointment</h1>
      <p class="subtitle">Find the right doctor and reserve a time slot</p>
    </div>

    <!-- Filters -->
    <div class="filters">
      <input
        v-model="search"
        @input="loadDoctors"
        placeholder="Search doctor name..."
      />

      <!-- Dynamic Specializations -->
      <select v-model="specialization" @change="loadDoctors">
        <option value="">All Departments</option>
        <option
          v-for="s in specializationss"
          :key="s.id"
          :value="s.id"
        >
          {{ s.name }}
        </option>
      </select>

      <select v-model="sort" @change="loadDoctors">
        <option value="">Sort by</option>
        <option value="fees_low">Fees: Low to High</option>
        <option value="fees_high">Fees: High to Low</option>
      </select>
    </div>

    <!-- Doctors Grid -->
    <div v-if="loading" class="loading">Loading doctors...</div>

    <div v-else class="grid">
      <DoctorCard v-if="doctors.length>0"
        v-for="doc in doctors"
        :key="doc.id"
        :doctor="doc"
        @details="openDetails"
        @book="openBooking"
      />
      <p v-else>No Doctors in this Department</p>
    </div>

    <!-- Modals -->
    <DoctorDetailsModal
      :show="showDetails"
      :doctor="selectedDoctor"
      @close="showDetails = false"
      @book="openBooking"
    />

    <SlotBookingModal
      :show="showSlots"
      :doctor="selectedDoctor"
      :slots="availableSlots"
      @close="showSlots = false"
      @select-slot="bookSlot"
    />
  </div>
</template>


<style scoped>

.page {
  padding: 26px;
  max-width: 1200px;
  margin: auto;
  
}


.header-block {
  background: linear-gradient(135deg, #6ad4c4, #4ea8de);
  padding: 26px 30px;
  border-radius: 18px;
  color: white;
  margin-bottom: 28px;
  box-shadow: 0 6px 22px rgba(0,0,0,0.1);
}

.title {
  font-size: 26px;
  font-weight: 800;
}

.subtitle {
  margin-top: 4px;
  opacity: 0.92;
}


.filters {
  display: flex;
  gap: 14px;
  margin-bottom: 22px;
  flex-wrap: wrap;
}

input,
select {
  padding: 12px 14px;
  border: 1px solid #cdd9e5;
  border-radius: 10px;
  background: white;
  font-size: 14px;
  width: 200px;
  transition: 0.2s ease;
}

input:focus,
select:focus {
  border-color: #4ea8de;
  box-shadow: 0 0 6px rgba(78,168,222,0.4);
}


.grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}


.loading {
  text-align: center;
  color: #7b8a97;
  padding: 20px;
  font-size: 18px;
}
</style>
