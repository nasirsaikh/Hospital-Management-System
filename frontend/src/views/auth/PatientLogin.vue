<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import authAPI from "@/api/auth/auth";
import { useAuthStore } from "@/store/auth";
import { useToast } from "@/utils/useToast";

import { User, Mail, Lock } from "lucide-vue-next";

const toast = useToast();

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const auth = useAuthStore();
const router = useRouter();

const login = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await authAPI.login({
      email: email.value,
      password: password.value,
      role: "patient"
    });

    auth.setAuth(res.data.token, "patient", res.data.user);
    router.push("/patient/dashboard");
    toast.success("Login Successful");

  } catch (err) {
    error.value = "Invalid patient credentials";
    toast.error("Login Failed");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="patient-login-page">

    <div class="login-card">


      <div class="icon-box">
        <User class="card-icon" />
      </div>

      <h2>Patient Login</h2>
      <p class="subtitle">Access appointments & medical history</p>


      <div class="input-group">
        <Mail class="input-icon" />
        <input v-model="email" placeholder="Email" />
      </div>


      <div class="input-group">
        <Lock class="input-icon" />
        <input v-model="password" type="password" placeholder="Password" />
      </div>

      <button @click="login" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>

      <p class="error" v-if="error">{{ error }}</p>

      <router-link to="/register" class="link">
        New patient? Register here
      </router-link>

    </div>

  </div>
</template>

<style scoped>
.patient-login-page {
  height: 100vh;
  background: linear-gradient(145deg, #e0f7fa, #b2ebf2, #80deea);
  display: flex;
  justify-content: center;
  align-items: center;
}


.login-card {
  width: 380px;
  padding: 34px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(14px);
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-align: center;
  color: #0f172a;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.35s ease;
}


.icon-box {
  width: 72px;
  height: 72px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-icon {
  width: 38px;
  height: 38px;
  color: #0077b6;
}


h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: #023047;
}

.subtitle {
  margin-top: 6px;
  margin-bottom: 22px;
  font-size: 14px;
  color: #457b9d;
}


.input-group {
  position: relative;
  margin-bottom: 14px;
}

.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #4b5563;
}

input {
  width: 85%;
  padding: 12px 12px 12px 40px;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid #b6c6d3;
  color: #1e293b;
  border-radius: 10px;
  font-size: 14px;
  transition: 0.2s;
}

input:focus {
  border-color: #0077b6;
  background: rgba(255, 255, 255, 0.9);
  outline: none;
}


button {
  width: 100%;
  margin-top: 8px;
  padding: 12px;
  background: #0077b6;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

button:hover {
  background: #005f88;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


.error {
  margin-top: 12px;
  color: #d00000;
  font-size: 14px;
}


.link {
  margin-top: 14px;
  display: block;
  color: #045b73;
  font-size: 14px;
  text-decoration: underline;
  transition: 0.2s;
}

.link:hover {
  color: #023047;
}


@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
