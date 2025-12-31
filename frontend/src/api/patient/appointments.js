import axios from "@/utils/axios";


export default {
  book(data) {
    return axios.post("/patient/appointments", data);
  },

  getMyAppointments() {
    return axios.get("/patient/appointments");
  },
  getAll() {
    return axios.get('/patient/appointments')
  },
  
  cancel(id) {
    return axios.put(`/patient/appointments/${id}/cancel`)
  }
};


