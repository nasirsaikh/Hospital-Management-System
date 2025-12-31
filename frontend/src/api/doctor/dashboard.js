import axios from "@/utils/axios";

export default {
  getDashboard() {
    return axios.get("/doctor/dashboard");
  }
};
