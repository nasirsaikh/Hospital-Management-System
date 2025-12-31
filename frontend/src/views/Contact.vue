<script setup>
import { Mail, Phone, MapPin } from "lucide-vue-next";
</script>

<template>
  <div class="contact">

    
    <section class="hero">
      <h1>Contact Us</h1>
      <p>We're here to help. Reach out anytime.</p>
    </section>

    
    <section class="info-section">

      
      <div class="info-card">
        <Mail class="icon" />
        <h3>Email</h3>
        <p>support@hospital.com</p>
      </div>

      
      <div class="info-card">
        <Phone class="icon" />
        <h3>Phone</h3>
        <p>+91 99999 99999</p>
      </div>

      
      <div class="info-card">
        <MapPin class="icon" />
        <h3>Address</h3>
        <p>Hazi Chowk, Ranchi, India</p>
      </div>

    </section>

    
    <section class="map-section">
      <iframe
        class="map"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.923708987387!2d77.5946!3d12.9716!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xabcdef!2sHospital!5e0!3m2!1sen!2sin!4v000000000"
      ></iframe>
    </section>

  </div>
</template>

<style scoped>
.contact {
  font-family: "Inter", sans-serif;
}

/* HERO */
.hero {
  text-align: center;
  padding: 70px 20px;
  background: linear-gradient(135deg, #e8f3ff, #ffffff);
}
.hero h1 {
  font-size: 38px;
  font-weight: 700;
  color: #1d3557;
}
.hero p {
  margin-top: 10px;
  font-size: 18px;
  color: #4a4a4a;
}

/* INFORMATION CARDS */
.info-section {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
  padding: 50px 20px;
}
.info-card {
  width: 260px;
  padding: 26px;
  border-radius: 14px;
  background: white;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  text-align: center;
  transition: 0.25s ease;
}
.info-card:hover {
  transform: translateY(-6px);
}

.icon {
  width: 48px;
  height: 48px;
  color: #1d3557;
  margin-bottom: 14px;
}

.info-card h3 {
  font-size: 18px;
  margin-bottom: 4px;
  color: #1d3557;
}
.info-card p {
  font-size: 15px;
  color: #444;
}

/* MAP */
.map-section {
  padding: 40px 20px;
  text-align: center;
}
.map {
  width: 100%;
  max-width: 900px;
  height: 350px;
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}
</style>
