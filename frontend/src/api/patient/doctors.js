import axios from "@/utils/axios";

export default {
  getAllDoctors(params = {}) {
    return axios.get("/patient/doctors", { params });
  },

  getAvailability(doctorId) {
    return axios.get(`/patient/doctors/${doctorId}/availability`);
  },

  getDoctorProfile(doctorId) {
    return axios.get(`/patient/doctors/${doctorId}`);
  },
};
