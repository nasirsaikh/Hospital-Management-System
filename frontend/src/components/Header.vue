<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const showDropdown = ref(false);

const logout = () => {
  auth.logout();
  router.push("/login/patient");
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};
</script>

<template>
  <header class="header">
    <div class="container">

      <div class="brand" @click="router.push('/')">
        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" alt="logo" />
        <span>Smart Hospital</span>
      </div>


      <nav class="nav">
        <router-link to="/">Home</router-link>
        <router-link to="/about">About Us</router-link>
        <router-link to="/contact">Contact Us</router-link>


        <button v-if="auth.token" class="logout-btn" @click="logout">
          Logout
        </button>


        <div v-if="!auth.token" class="login-dropdown-wrapper">
          <button class="login-btn" @click="toggleDropdown">
            Login ▾
          </button>

          <div v-if="showDropdown" class="dropdown">
            <button @click="router.push('/login/patient')">Patient Login</button>
            <button @click="router.push('/login/doctor')">Doctor Login</button>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  z-index: 1000;
  position: sticky;
  top: 0;
  background: #1d3557;
  padding: 14px 0;
  color: white;
  border-bottom: 2px solid #0f2238;
}

.container {
  width: 92%;
  max-width: 1200px;
  margin: auto;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
  font-size: 22px;
  font-weight: 600;
  cursor: pointer;
}

.brand img {
  width: 36px;
  opacity: 0.9;
}

.nav {
  display: flex;
  align-items: center;
  gap: 22px;
  position: relative;
}

.nav a {
  color: white;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: 0.2s;
}

.nav a:hover {
  opacity: 0.75;
}

.logout-btn,
.login-btn {
  padding: 8px 18px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.logout-btn {
  background: #e63946;
  color: white;
}

.logout-btn:hover {
  background: #d62839;
}

.login-btn {
  background: white;
  color: #1d3557;
  border-radius: 4px;
}

.login-btn:hover {
  background: #dce1e8;
}

.login-dropdown-wrapper {
  position: relative;
}

/* Dropdown box */
.dropdown {
  position: absolute;
  top: 44px;
  right: 0;
  width: 170px;

  background: white;
  border-radius: 6px;
  padding: 8px 0;

  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.18);
  z-index: 20;
}

.dropdown button {
  width: 100%;
  padding: 10px 14px;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;

  font-size: 14px;
  color: #1d3557;
}

.dropdown button:hover {
  background: #eef2f5;
}
</style>
