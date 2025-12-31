<script setup>
</script>

<template>
  <div class="about">

    
    <section class="hero">
      <h1>About Our Hospital Management System</h1>
      <p>
        Empowering hospitals with intelligent, seamless, and human-centered technology.
      </p>
    </section>

    
    <section class="story">
      <h2>Our Mission</h2>
      <p>
        We aim to modernize healthcare management by building powerful tools that help doctors,
        patients, and administrators work together effortlessly.  
        Our system eliminates inefficiencies, improves communication, and ensures that every
        stakeholder has the information they need.
      </p>

      <h2>Our Vision</h2>
      <p>
        A future where hospitals run like well-orchestrated symphonies — smooth, fast, connected,
        and stress-free. Technology should amplify care, never complicate it.
      </p>
    </section>

    
    <section class="values">
      <h2>What We Stand For</h2>

      <div class="value-grid">
        <div class="value-card">
          <img src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png" />
          <h3>Reliability</h3>
          <p>Your data, workflows, and communication — always available.</p>
        </div>

        <div class="value-card">
          <img src="https://cdn-icons-png.flaticon.com/512/1828/1828673.png" />
          <h3>Care</h3>
          <p>We design everything to prioritize people, not systems.</p>
        </div>

        <div class="value-card">
          <img src="https://cdn-icons-png.flaticon.com/512/1828/1828919.png" />
          <h3>Innovation</h3>
          <p>Modern ideas and technologies tuned for real hospital needs.</p>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.about {
  font-family: "Inter", sans-serif;
}

/* HERO */
.hero {
  padding: 70px 30px;
  text-align: center;
  background: linear-gradient(135deg, #e8f3ff, #ffffff);
}
.hero h1 {
  font-size: 40px;
  font-weight: 700;
  color: #1d3557;
}
.hero p {
  margin-top: 12px;
  font-size: 18px;
  color: #4a4a4a;
}

/* STORY */
.story {
  max-width: 900px;
  margin: 60px auto;
  padding: 0 30px;
}
.story h2 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #1d3557;
}
.story p {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 30px;
  color: #444;
}

/* VALUES */
.values {
  padding: 60px 20px;
  background: #f7f9fc;
  text-align: center;
}
.values h2 {
  font-size: 30px;
  margin-bottom: 40px;
  color: #1d3557;
}
.value-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 26px;
}
.value-card {
  width: 260px;
  padding: 26px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
  transition: 0.25s;
  text-align: center;
}
.value-card:hover {
  transform: translateY(-5px);
}
.value-card img {
  width: 60px;
  margin-bottom: 12px;
}
.value-card h3 {
  font-size: 18px;
  color: #1d3557;
  margin-bottom: 6px;
}
.value-card p {
  font-size: 14px;
  color: #444;
}
</style>
