import axios from "@/utils/axios";

export default {
  getAllPatients() {
    return axios.get("/admin/patients");
  },

  getPatient(id) {
    return axios.get(`/admin/patients/${id}`);
  },

  updatePatient(id, data) {
    return axios.put(`/admin/patients/${id}`, data);
  },

  deletePatient(id) {
    return axios.delete(`/admin/patients/${id}`);
  },

  togglePatientStatus(id) {
    return axios.put(`/admin/patients/${id}/toggle`);
  }
};
