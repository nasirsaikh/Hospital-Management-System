import axios from "@/utils/axios";

export default {
  getAll(filters = {}) {
    return axios.get("/doctor/appointments", { params: filters });
  },

  getOne(id) {
    return axios.get(`/doctor/appointments/${id}`);
  },

  update(id, payload) {
    return axios.put(`/doctor/appointments/${id}`, payload);
  },

  markComplete(id) {
    return axios.put(`/doctor/appointments/${id}`, {
      status: "completed",
    });
  },
};
