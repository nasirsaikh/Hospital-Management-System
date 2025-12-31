import axios from "@/utils/axios";

export default {
  dashboard() {
    return axios.get("/admin/dashboard");
  },

  getDoctors() {
    return axios.get("/admin/doctors");
  },

  addDoctor(data) {
    return axios.post("/admin/doctors", data);
  },

  updateDoctor(id, data) {
    return axios.put(`/admin/doctors/${id}`, data);
  },

  deleteDoctor(id) {
    return axios.delete(`/admin/doctors/${id}`);
  },

  getPatients() {
    return axios.get("/admin/patients");
  },

  toggleBlockPatient(id, data) {
    return axios.put(`/admin/patients/${id}/block`, data);
  },


  getAppointments() {
    return axios.get("/admin/appointments");
  },
  
  updateAppointmentStatus(id, data) {
    return axios.put(`/admin/appointments/${id}/status`, data);
  },


  getSpecializations() {
    return axios.get("/admin/specializations");
  },

  addSpecialization(data) {
    return axios.post("/admin/specializations", data);
  },
  getSpecializations() {
    return axios.get("/admin/specializations");
  },

  addSpecialization(data) {
    return axios.post("/admin/specializations", data);
  },

  deleteSpecialization(id) {
    return axios.delete(`/admin/specializations/${id}`);
  },
  getPatientHistory(patientId) {
  return axios.get(`/admin/patients/${patientId}/records`);
},


};
