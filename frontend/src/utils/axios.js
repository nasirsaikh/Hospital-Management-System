import axios from "axios";
import { useAuthStore } from "@/store/auth";

const instance = axios.create({
  baseURL: "http://localhost:5050",
  withCredentials: false
});

// Attach token to requests
instance.interceptors.request.use((config) => {
  const auth = useAuthStore();

  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;
  }

  return config;
});

// Global error handling (401 token expired)
instance.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      const auth = useAuthStore();
      auth.logout();
      window.location.href = "/patient/login";
    }
    return Promise.reject(err);
  }
);

export default instance;
