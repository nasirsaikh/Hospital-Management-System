<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import authAPI from "@/api/auth/auth";
import { useAuthStore } from "@/store/auth";
import { useToast } from "@/utils/useToast";

import { Shield, Mail, Lock } from "lucide-vue-next";

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
      role: "admin",
    });

    auth.setAuth(res.data.token, "admin", res.data.user);
    toast.success("Login Successful");
    router.push("/admin/dashboard");
  } catch (err) {
    error.value = "Invalid admin credentials";
    toast.error("Login Failed");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="admin-login-page">

    <div class="login-card">
      <div class="icon-box">
        <Shield class="shield-icon" />
      </div>

      <h2>Admin Login</h2>
      <p class="subtitle">Access your control panel securely</p>

      <div class="input-group">
        <Mail class="input-icon" />
        <input v-model="email" placeholder="Email" type="email" />
      </div>

      <div class="input-group">
        <Lock class="input-icon" />
        <input v-model="password" placeholder="Password" type="password" />
      </div>

      <button @click="login" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>

  </div>
</template>

<style scoped>
.admin-login-page {
  height: 100vh;
  background: radial-gradient(circle at top, #1f2937, #0f172a 70%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}


.login-card {
  width: 380px;
  padding: 34px;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(18px);
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 35px rgba(0, 0, 0, 0.4);
  text-align: center;
  color: #e5e7eb;
  animation: fadeIn 0.4s ease;
}


.icon-box {
  background: rgba(255, 255, 255, 0.08);
  width: 70px;
  height: 70px;
  margin: 0 auto 18px auto;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shield-icon {
  width: 38px;
  height: 38px;
  color: #60a5fa;
}


h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
}

.subtitle {
  opacity: 0.75;
  margin-top: 6px;
  margin-bottom: 22px;
  font-size: 14px;
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
  width: 90%;
  padding: 12px 12px 12px 40px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  color: #e5e7eb;
  font-size: 14px;
}

input:focus {
  border-color: #60a5fa;
  outline: none;
  background: rgba(255, 255, 255, 0.12);
}


button {
  width: 100%;
  padding: 12px;
  margin-top: 6px;
  border: none;
  border-radius: 10px;
  background: #3b82f6;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

button:hover {
  background: #2563eb;
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
