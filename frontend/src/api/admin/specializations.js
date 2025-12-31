import axios from "@/utils/axios";

export default {
  getAll() {
    return axios.get("/admin/specializations");
  },

  create(data) {
    return axios.post("/admin/specializations", data);
  },

  update(id, data) {
    return axios.put(`/admin/specializations/${id}`, data);
  },

  delete(id) {
    return axios.delete(`/admin/specializations/${id}`);
  }
};
