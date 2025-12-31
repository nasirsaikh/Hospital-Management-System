<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const goToLogin = () => router.push("/login/patient");
const goToRegister = () => router.push("/register");
</script>

<template>
  <div class="home">

    <!-- HERO SECTION -->
    <section class="hero">
      <div class="hero-left">


        <h1>
          Smart Hospital Management  
          <span class="gradient-text">Reimagined</span>
        </h1>

        <p class="subtitle">
          A next-gen digital healthcare system powered by seamless workflows,
          modern automation, and Vue magic.
        </p>

        <div class="hero-buttons">
          <button class="btn primary" @click="goToLogin">Login</button>
          <button class="btn secondary" @click="goToRegister">Register</button>
        </div>
      </div>

      <div class="hero-right">
        <img
          src="https://cdn-icons-png.flaticon.com/512/2966/2966486.png"
          alt="Hospital"
          class="hero-illustration"
        />
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <h2 class="section-title">Powerful Tools, Simple Interface</h2>

      <div class="feature-grid">

        <div class="feature-card">
          <img src="https://cdn-icons-png.flaticon.com/512/2913/2913597.png" />
          <h3>Instant Appointments</h3>
          <p>Find doctors, view availability, and book in seconds.</p>
        </div>

        <div class="feature-card">
          <img src="https://cdn-icons-png.flaticon.com/512/2966/2966480.png" />
          <h3>Doctor Workspace</h3>
          <p>Manage daily schedules, patient records, and reports.</p>
        </div>

        <div class="feature-card">
          <img src="https://cdn-icons-png.flaticon.com/512/3004/3004613.png" />
          <h3>Unified Medical Records</h3>
          <p>Diagnostics, prescriptions, notes — organized beautifully.</p>
        </div>

        <div class="feature-card">
          <img src="https://cdn-icons-png.flaticon.com/512/992/992651.png" />
          <h3>Admin Control Center</h3>
          <p>Doctors, departments, analytics — complete oversight.</p>
        </div>

      </div>
    </section>

    <!-- WORKFLOW -->
    <section class="workflow">
      <h2 class="section-title">How Everything Connects</h2>

      <div class="flow-grid">
        <div class="flow-step">
          <span class="step-number">1</span>
          <h3>Register & Setup</h3>
          <p>Create an account and access your custom dashboard.</p>
        </div>

        <div class="flow-step">
          <span class="step-number">2</span>
          <h3>Connect With Doctors</h3>
          <p>Select specializations, browse schedules, and book.</p>
        </div>

        <div class="flow-step">
          <span class="step-number">3</span>
          <h3>View Reports & History</h3>
          <p>Your full medical history stays synced across devices.</p>
        </div>
      </div>
    </section>


  </div>
</template>


<style scoped>
.home {
  font-family: "Inter", sans-serif;
  color: #2b2b2b;
  overflow-x: hidden;
}

/* HERO */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 80px 70px;
  background: linear-gradient(135deg, #e8f4ff, #ffffff);
}

.vue-logo {
  width: 70px;
  margin-bottom: 15px;
  opacity: 0.92;
}

.hero-left {
  max-width: 520px;
}

.hero-left h1 {
  font-size: 48px;
  font-weight: 800;
  line-height: 1.1;
  color: #1d3557;
}

.gradient-text {
  background: linear-gradient(90deg, #1d3557, #457b9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 18px;
  margin: 16px 0 28px;
  color: #555;
}

.hero-buttons {
  display: flex;
  gap: 16px;
}

.hero-illustration {
  width: 400px;
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
  100% { transform: translateY(0px); }
}

/* BUTTONS */
.btn {
  padding: 12px 26px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: 0.25s;
}

.btn.primary {
  background: #1d3557;
  color: white;
}
.btn.primary:hover {
  background: #152b45;
}

.btn.secondary {
  background: white;
  border: 2px solid #1d3557;
  color: #1d3557;
}
.btn.secondary:hover {
  background: #1d3557;
  color: white;
}

.big {
  padding: 14px 34px;
  font-size: 17px;
}

/* SECTION TITLE */
.section-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin: 50px 0;
  color: #1d3557;
}

/* FEATURES */
.features {
  padding: 20px 50px 70px;
  background: #f7f9fc;
}

.feature-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 26px;
  justify-content: center;
}

.feature-card {
  width: 260px;
  padding: 24px;
  border-radius: 14px;
  background: white;
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
  transition: 0.25s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-7px);
}

.feature-card img {
  width: 70px;
  margin-bottom: 12px;
}

/* WORKFLOW */
.workflow {
  padding: 70px 50px;
  background: linear-gradient(145deg, #ffffff, #e9f3ff);
}

.flow-grid {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.flow-step {
  background: white;
  padding: 24px;
  width: 260px;
  border-radius: 14px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.06);
  text-align: center;
  transition: 0.25s ease;
}

.flow-step:hover {
  transform: translateY(-6px);
}

.step-number {
  background: #1d3557;
  color: white;
  padding: 8px 14px;
  border-radius: 50%;
  font-weight: 700;
  font-size: 17px;
  display: inline-block;
  margin-bottom: 10px;
}

/* CTA */
.cta {
  text-align: center;
  padding: 80px 20px;
  background: #1d3557;
  color: white;
}

.cta h2 {
  font-size: 34px;
  font-weight: 700;
}

.cta p {
  margin: 10px 0 20px;
  opacity: 0.9;
}

</style>
