import axios from "@/utils/axios";

export default {
  getAll() {
    return axios.get("/patient/records");
  },
  startExport() {
    return axios.post("/patient/export-treatments");
  },
};
