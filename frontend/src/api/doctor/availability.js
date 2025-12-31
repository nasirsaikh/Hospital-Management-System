import axios from "@/utils/axios";


export default {
  getAll() {
    return axios.get("/doctor/availability");
  },
  
  save(payload) {
    return axios.post("/doctor/availability", payload);
  },
};

