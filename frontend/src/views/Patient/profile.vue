<script setup>
import { ref, onMounted } from "vue";
import profileAPI from "@/api/patient/profile";
import { useToast } from "@/utils/useToast";
import { useAuthStore } from "@/store/auth";

const toast = useToast();
const auth = useAuthStore();

const loading = ref(true);
const saving = ref(false);

const form = ref({
  name: "",
  age: "",
  gender: "",
  phone: "",
  address: "",
});

onMounted(async () => {
  try {
    const res = await profileAPI.getProfile();
    form.value = {
      name: res.data.name,
      age: res.data.age || "",
      gender: res.data.gender || "",
      phone: res.data.phone || "",
      address: res.data.address || "",
    };
  } catch (e) {
    toast.error("Unable to load profile");
  }
  loading.value = false;
});

const saveProfile = async () => {
  saving.value = true;
  try {
    await profileAPI.updateProfile({ ...form.value });
    toast.success("Profile updated");

    auth.setUser({ ...auth.user, name: form.value.name });
  } catch (e) {
    toast.error("Update failed");
  }
  saving.value = false;
};
</script>

<template>
  <div class="page">

    <!-- Header Banner -->
    <div class="header-block">
      <h1 class="title">My Profile</h1>
      <p class="subtitle">Manage your personal information</p>
    </div>

    <!-- Loader -->
    <div v-if="loading" class="loading-wrap">
      <div class="loader"></div>
      Loading profile...
    </div>

    <!-- Profile Form -->
    <div v-else class="profile-card">

      <!-- Avatar -->
      <div class="avatar">
        {{ form.name?.charAt(0)?.toUpperCase() || "P" }}
      </div>

      <!-- Editable Form -->
      <div class="form">

        <label>Name</label>
        <input v-model="form.name" placeholder="Your name" />

        <label>Age</label>
        <input v-model="form.age" type="number" min="1" />

        <label>Gender</label>
        <select v-model="form.gender">
          <option disabled value="">Select gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>

        <label>Phone</label>
        <input v-model="form.phone" placeholder="Phone number" />

        <label>Address</label>
        <textarea v-model="form.address" rows="3"></textarea>

      </div>

      <!-- Save Button -->
      <button class="save-btn" :disabled="saving" @click="saveProfile">
        {{ saving ? "Saving..." : "Save Changes" }}
      </button>

    </div>

  </div>
</template>

<style scoped>
.page {
  padding: 26px;
  max-width: 750px;
  margin: auto;
}


.header-block {
  background: linear-gradient(135deg, #6ad4c4, #4ea8de);
  padding: 26px;
  border-radius: 18px;
  margin-bottom: 26px;
  color: white;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

.title { font-size: 28px; font-weight: 800; }
.subtitle { margin-top: 3px; opacity: 0.92; }


.loading-wrap { text-align: center; padding-top: 40px; }


.profile-card {
  background: #fff;
  padding: 24px;
  border-radius: 18px;
  box-shadow: 0 3px 14px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}


.avatar {
  width: 90px; height: 90px;
  background: #4ea8de;
  border-radius: 50%;
  color: white;
  font-size: 34px;
  display: grid;
  place-items: center;
  font-weight: 700;
}


.form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
label { font-weight: 600; font-size: 14px; }

input, select, textarea {
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ced6dd;
  font-size: 15px;
}
input:focus, select:focus, textarea:focus {
  border-color: #4ea8de;
  box-shadow: 0 0 0 2px rgba(78,168,222,0.15);
}


.save-btn {
  margin-top: 10px;
  background: #4ea8de;
  color: white;
  padding: 12px 18px;
  border-radius: 12px;
  width: 100%;
  font-size: 16px;
  font-weight: 700;
  border: none;
  cursor: pointer;
}
.save-btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
