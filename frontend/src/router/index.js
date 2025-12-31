// ============================
// VUE & STORE
// ============================
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// ============================
// GENERAL PAGES
// ============================
import Home from '@/views/Home.vue'
import AboutUs from '@/views/AboutUs.vue'
import Contact from '@/views/Contact.vue'

// ============================
// AUTH PAGES
// ============================
import Register from '@/views/auth/Register.vue'
import PatientLogin from '@/views/auth/PatientLogin.vue'
import DoctorLogin from '@/views/auth/DoctorLogin.vue'
import AdminLogin from '@/views/auth/AdminLogin.vue'

// ============================
// ADMIN PAGES
// ============================
import AdminDashboard from '@/views/admin/Admindashboard.vue'
import DoctorsList from '@/views/Admin/doctors/DoctorsList.vue'
import AddDoctor from '@/views/Admin/doctors/AddDoctor.vue'
import EditDoctor from '@/views/Admin/doctors/EditDoctor.vue'
import PatientList from '@/views/Admin/patients/PatientList.vue'
import PatientEdit from '@/views/Admin/patients/PatientEdit.vue'
import AppointmentsList from '@/views/Admin/appointments/AppointmentsList.vue'
import SpecializationList from '@/views/Admin/specializations/SpecializationList.vue'
import SpecializationCreate from '@/views/Admin/specializations/SpecializationCreate.vue'
import SpecializationEdit from '@/views/Admin/specializations/SpecializationEdit.vue'

// ============================
// PATIENT PAGES
// ============================
import PatientDashboard from '@/views/patient/Patientdashboard.vue'
import BookAppointments from '@/views/patient/BookAppointments.vue'
import MyAppointments from '@/views/patient/MyAppointments.vue'
import Records from '@/views/patient/records.vue'
import Profile from '@/views/patient/profile.vue'

// ============================
// DOCTOR PAGES
// ============================
import DoctorDashboard from '@/views/doctor/Doctordashboard.vue'
import DoctorAvailability from '@/views/doctor/DoctorAvailability.vue'
import DoctorAppointment from '@/views/doctor/DoctorAppointment.vue'


// ============================
// ROUTES
// ============================
const routes = [
  // General
  { path: "/", component: Home },
  { path: "/about", component: AboutUs },
  { path: "/contact", component: Contact },

  // Auth
  { path: "/register", component: Register },
  { path: "/login/patient", component: PatientLogin },
  { path: "/login/doctor", component: DoctorLogin },
  { path: "/login/admin", component: AdminLogin },

  // Admin
  { path: "/admin/dashboard", component: AdminDashboard },
  { path: "/admin/doctors", component: DoctorsList },
  { path: "/admin/doctors/add", component: AddDoctor },
  { path: "/admin/doctors/edit/:id", component: EditDoctor },
  { path: "/admin/patients", component: PatientList },
  { path: "/admin/patients/:id/edit", component: PatientEdit },
  { path: "/admin/appointments", component: AppointmentsList },
  { path: "/admin/specializations", component: SpecializationList },
  { path: "/admin/specializations/create", component: SpecializationCreate },
  { path: "/admin/specializations/:id/edit", component: SpecializationEdit },

  // Patient
  { path: "/patient/dashboard", component: PatientDashboard },
  { path: "/patient/book", component: BookAppointments },
  { path: "/patient/appointments", component: MyAppointments },
  { path: "/patient/records", component: Records },
  { path: "/patient/profile", component: Profile },

  // Doctor
  { path: "/doctor/dashboard", component: DoctorDashboard },
  { path: "/doctor/availability", component: DoctorAvailability },
  { path: "/doctor/appointments", component: DoctorAppointment },
]


// ============================
// ROUTER SETUP
// ============================
const router = createRouter({
  history: createWebHistory(),
  routes,
})


// ============================
// NAVIGATION GUARD
// ============================
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  const publicPages = [
    "/", "/login/patient", "/login/doctor", "/login/admin",
    "/register", "/about", "/contact"
  ]

  if (!auth.token && publicPages.includes(to.path)) {
    return next()
  }

  if (!auth.token && !publicPages.includes(to.path)) {
    return next("/")
  }

  if (to.meta.role && to.meta.role !== auth.role) {
    return next("/dashboard")
  }

  next()
})


export default router
