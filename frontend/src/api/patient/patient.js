import axios from "@/utils/axios";

export default {
  dashboard() {
    return axios.get("/patient/dashboard");
  },

  getAppointments() {
    return axios.get("/patient/appointments");
  },

  getAppointment(id) {
    return axios.get(`/patient/appointments/${id}`);
  },

  bookAppointment(data) {
    return axios.post("/patient/appointments", data);
  },

  getDoctors() {
    return axios.get("/patient/doctors");
  },

  getDoctorAvailability(doctorId, date) {
    return axios.get(`/patient/doctors/${doctorId}/availability`, {
      params: { date },
    });
  },

  getRecords() {
    return axios.get("/patient/records");
  },

  getRecord(id) {
    return axios.get(`/patient/records/${id}`);
  },

  getProfile() {
    return axios.get("/patient/profile");
  },

  updateProfile(data) {
    return axios.put("/patient/profile", data);
  },
};
