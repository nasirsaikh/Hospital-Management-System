<script setup>
import { ref, reactive } from "vue";
import authAPI from "@/api/auth/auth";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { useToast } from "@/utils/useToast";

import { User, Mail, Lock, Phone, MapPin, Calendar, UserPlus } from "lucide-vue-next";

const toast = useToast();
const router = useRouter();
const auth = useAuthStore();

const form = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  age: "",
  gender: "",
  phone: "",
  address: "",
});

const errors = reactive({});
const loading = ref(false);
const apiError = ref("");


const validate = () => {
  apiError.value = "";
  Object.keys(errors).forEach((k) => (errors[k] = ""));
  let ok = true;

  if (!form.name.trim()) { errors.name = "Full name required"; ok = false; }

  if (!form.email.trim()) {
    errors.email = "Email required"; ok = false;
  } else if (!/^\S+@\S+\.\S+$/.test(form.email)) {
    errors.email = "Enter valid email"; ok = false;
  }

  if (!form.password) {
    errors.password = "Password required"; ok = false;
  } else if (form.password.length < 6) {
    errors.password = "Min 6 characters"; ok = false;
  }

  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = "Passwords mismatch"; ok = false;
  }

  if (!form.age || Number(form.age) <= 0) {
    errors.age = "Enter valid age"; ok = false;
  }

  if (!form.gender) { errors.gender = "Select gender"; ok = false; }

  if (!form.phone.trim()) {
    errors.phone = "Phone required"; ok = false;
  }

  if (!form.address.trim()) {
    errors.address = "Address required"; ok = false;
  }

  return ok;
};


const register = async () => {
  if (!validate()) return;
  loading.value = true;

  try {
    const res = await authAPI.register({
      name: form.name,
      email: form.email,
      password: form.password,
      age: form.age,
      gender: form.gender,
      phone: form.phone,
      address: form.address,
    });

    toast.success("Registered Successfully!");


    auth.setAuth(res.data.token, res.data.role);
    router.push("/patient/dashboard");

  } catch (e) {
    apiError.value = e?.response?.data?.message || "Registration failed";
    toast.error("Registration Failed");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="register-page">

    <div class="glass-card">


      <div class="left">
        <UserPlus class="big-icon" />
        <h1>Create Your Patient Account</h1>
        <p class="tagline">
          Join our smart healthcare system and take control of your medical journey.
        </p>

        <ul class="features">
          <li>Easy appointment booking</li>
          <li>Access digital records anytime</li>
          <li>Track doctor visits & prescriptions</li>
        </ul>
      </div>


      <div class="right">
        <form @submit.prevent="register">


          <div class="row">
            <div class="field">
              <label>Name</label>
              <div class="input-group">
                <User class="icon" />
                <input v-model="form.name" placeholder="Full Name" />
              </div>
              <p v-if="errors.name" class="error">{{ errors.name }}</p>
            </div>

            <div class="field">
              <label>Email</label>
              <div class="input-group">
                <Mail class="icon" />
                <input v-model="form.email" placeholder="Email Address" />
              </div>
              <p v-if="errors.email" class="error">{{ errors.email }}</p>
            </div>
          </div>


          <div class="row">
            <div class="field">
              <label>Password</label>
              <div class="input-group">
                <Lock class="icon" />
                <input type="password" v-model="form.password" placeholder="Password" />
              </div>
              <p v-if="errors.password" class="error">{{ errors.password }}</p>
            </div>

            <div class="field">
              <label>Confirm Password</label>
              <div class="input-group">
                <Lock class="icon" />
                <input type="password" v-model="form.confirmPassword" placeholder="Confirm" />
              </div>
              <p v-if="errors.confirmPassword" class="error">{{ errors.confirmPassword }}</p>
            </div>
          </div>


          <div class="row">
            <div class="field small">
              <label>Age</label>
              <div class="input-group">
                <Calendar class="icon" />
                <input type="number" v-model="form.age" placeholder="Age" />
              </div>
              <p v-if="errors.age" class="error">{{ errors.age }}</p>
            </div>

            <div class="field small">
              <label>Gender</label>
              <select v-model="form.gender">
                <option disabled value="">Select</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
              <p v-if="errors.gender" class="error">{{ errors.gender }}</p>
            </div>

            <div class="field">
              <label>Phone</label>
              <div class="input-group">
                <Phone class="icon" />
                <input v-model="form.phone" placeholder="Phone Number" />
              </div>
              <p v-if="errors.phone" class="error">{{ errors.phone }}</p>
            </div>
          </div>


          <div class="field">
            <label>Address</label>
            <div class="input-group textarea">
              <MapPin class="icon top" />
              <textarea rows="2" v-model="form.address" placeholder="Full Address"></textarea>
            </div>
            <p v-if="errors.address" class="error">{{ errors.address }}</p>
          </div>

          <p v-if="apiError" class="error global">{{ apiError }}</p>

          <button class="btn" :disabled="loading">
            {{ loading ? "Creating Account..." : "Create Account" }}
          </button>

          <p class="login-text">
            Already have an account?
            <router-link to="/login/patient">Login</router-link>
          </p>

        </form>
      </div>
    </div>

  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(145deg, #c8f4f8, #a8e6ec, #7ddce6);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}


.glass-card {
  display: flex;
  gap: 32px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 32px;
  max-width: 1100px;
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.15);
}


.left {
  flex: 1;
  padding-right: 24px;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
}

.big-icon {
  width: 62px;
  height: 62px;
  color: #0077b6;
  margin-bottom: 12px;
}

.left h1 {
  color: #023047;
  margin-bottom: 8px;
  font-size: 26px;
  font-weight: 700;
}

.tagline {
  color: #374151;
  margin-bottom: 18px;
}

.features {
  font-size: 15px;
  color: #1f2937;
}


.right {
  flex: 1.2;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}


.row {
  display: flex;
  gap: 16px;
}


.field {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.field.small {
  max-width: 160px;
}

label {
  font-size: 13px;
  margin-bottom: 5px;
  color: #023047;
}


.input-group {
  position: relative;
  max-width: 85%;
}

.input-group.textarea {
  align-items: start;
  max-width: 100%;
}

.icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 12px;
  width: 18px;
  height: 18px;
  color: #374151;
}

.icon.top {
  top: 14px;
}

input,
select,
textarea {
  width: 85%;
  padding: 10px 12px 10px 40px;
  border: 1px solid #b9c7d3;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  color: #1e293b;
}


textarea {
  padding-top: 34px;
}


.error {
  margin-top: 4px;
  font-size: 12px;
  color: #b91c1c;
}

.error.global {
  text-align: center;
}


.btn {
  margin-top: 4px;
  background: #0077b6;
  padding: 12px;
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn:hover {
  background: #005f88;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


.login-text {
  text-align: center;
  font-size: 14px;
}

.login-text a {
  color: #023047;
  font-weight: 600;
}


@media (max-width: 900px) {
  .glass-card {
    flex-direction: column;
    padding: 24px;
  }

  .left {
    border-right: none;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding-bottom: 14px;
  }
}
</style>
