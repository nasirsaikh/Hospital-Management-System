import axios from "@/utils/axios"

export default {
  
  save(data) {
    
    return axios.post("/doctor/records", data);
  },

  
  getOne(appointmentId) {
    return axios.get(`/doctor/records/${appointmentId}`);
  },
  getPatientRecords(patientId) {
    return axios.get(`/doctor/patients/${patientId}/records`);
  }
};


