import axios from "@/utils/axios";

export default {
  getAll() {
    return axios.get("/admin/doctors");
  },

  get(id) {
    return axios.get(`/admin/doctors/${id}`);
  },

  create(data) {
    return axios.post("/admin/doctors", data);
  },

  update(id, data) {
    return axios.put(`/admin/doctors/${id}`, data);
  },

  delete(id) {
    return axios.delete(`/admin/doctors/${id}`);
  },

  verify(id) {
    return axios.put(`/admin/doctors/${id}/verify`);
  },

  toggle(id) {
    return axios.post(`/admin/doctors/${id}/toggle`);
  },

  getAvailability(id) {
    return axios.get(`/admin/doctors/${id}/availability`);
  },

  addAvailability(id, data) {
    return axios.post(`/admin/doctors/${id}/availability`, data);
  },

  deleteAvailability(id, slotId) {
    return axios.delete(`/admin/doctors/${id}/availability/${slotId}`);
  },
  getSpecializations() {
    return axios.get("/admin/specializations");
  },
  toggleStatus(id) {
    return axios.put(`/admin/doctors/${id}/toggle-status`);
  },
};
