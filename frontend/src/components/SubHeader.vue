<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/store/auth";

const auth = useAuthStore();

const role = computed(() => auth.role?.toUpperCase());



const patientMenu = [
  { name: "Dashboard", path: "/patient/dashboard" },
  { name: "Book Appointment", path: "/patient/book" },
  { name: "My Appointments", path: "/patient/appointments" },
  { name: "Records", path: "/patient/records" },
  { name: "Profile", path: "/patient/profile" }
];

const doctorMenu = [
  { name: "Dashboard", path: "/doctor/dashboard" },
  { name: "Availability", path: "/doctor/availability" },
  { name: "Appointments", path: "/doctor/appointments" },


];

const adminMenu = [
  { name: "Dashboard", path: "/admin/dashboard" },
  { name: "Doctors", path: "/admin/doctors" },
  { name: "Department", path: "/admin/specializations" },
  { name: "Patients", path: "/admin/patients" },
  { name: "Appointments", path: "/admin/appointments" },

];

const activeMenu = computed(() => {
  if (role.value === "PATIENT") return patientMenu;
  if (role.value === "DOCTOR") return doctorMenu;
  if (role.value === "ADMIN") return adminMenu;
  return [];
});
</script>

<template>
  <section v-if="auth.token" class="subheader">
    <div class="inner">


      <div class="role-badge">
        {{ role }}
      </div>


      <nav class="menu">
        <router-link v-for="item in activeMenu" :key="item.path" class="menu-item" :to="item.path"
          active-class="active">
          {{ item.name }}
        </router-link>
      </nav>

    </div>
  </section>
</template>

<style scoped>
.subheader {
  position: sticky;
  top: 64px;
  z-index: 9;

  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);

  border-bottom: 1px solid rgba(0, 0, 0, 0.08);

  padding: 10px 0;
}

.inner {
  max-width: 1200px;
  margin: auto;
  padding: 0 18px;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.role-badge {
  padding: 6px 12px;
  background: linear-gradient(135deg, #1d3557, #264a7c);
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.menu {
  display: flex;
  gap: 14px;
  align-items: center;
  overflow-x: auto;
}

.menu-item {
  padding: 6px 14px;
  border-radius: 20px;

  font-size: 14px;
  font-weight: 500;
  color: #334155;
  text-decoration: none;

  transition: 0.25s ease;
  border: 1px solid transparent;
}

.menu-item:hover {
  background: rgba(29, 53, 87, 0.07);
  color: #1d3557;
}

.active {
  background: #1d3557 !important;
  color: white !important;
  border-color: #1d3557 !important;
}
</style>
