<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import authAPI from "@/api/auth/auth";
import { useAuthStore } from "@/store/auth";
import { useToast } from "@/utils/useToast";

import { Stethoscope, Mail, Lock } from "lucide-vue-next";

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
      role: "doctor",
    });

    auth.setAuth(res.data.token, "doctor", res.data.user);
    toast.success("Login Successful");
    router.push("/doctor/dashboard");

  } catch (err) {
    error.value = "Invalid doctor credentials";
    toast.error("Login Failed");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="doctor-login-page">

    <div class="login-card">

      <div class="icon-box">
        <Stethoscope class="doc-icon" />
      </div>

      <h2>Doctor Login</h2>
      <p class="subtitle">Manage appointments, patients & medical records</p>


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

    </div>
  </div>
</template>

<style scoped>
.doctor-login-page {
  height: 100vh;
  background: radial-gradient(circle at top, #0f172a, #1e293b 70%);
  display: flex;
  justify-content: center;
  align-items: center;
}


.login-card {
  width: 380px;
  padding: 34px;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(16px);
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
  color: #e5e7eb;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
  animation: fadeIn 0.35s ease;
}


.icon-box {
  width: 72px;
  height: 72px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px auto;
}

.doc-icon {
  width: 40px;
  height: 40px;
  color: #4ade80;
}


h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
}

.subtitle {
  margin-top: 6px;
  margin-bottom: 22px;
  font-size: 14px;
  opacity: 0.75;
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
  color: #9ca3af;
}

input {
  width: 85%;
  padding: 12px 12px 12px 40px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.08);
  color: #e5e7eb;
  font-size: 14px;
  transition: 0.2s ease;
}

input:focus {
  border-color: #4ade80;
  background: rgba(255, 255, 255, 0.12);
  outline: none;
}


button {
  width: 100%;
  margin-top: 6px;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: #4ade80;
  color: #0f172a;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

button:hover {
  background: #22c55e;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


.error {
  margin-top: 12px;
  color: #f87171;
  font-size: 14px;
}


@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
