import axios from "@/utils/axios";

export default {
  getProfile() {
    return axios.get("/patient/profile");
  },

  updateProfile(data) {
    return axios.put("/patient/profile", data);
  },
};
