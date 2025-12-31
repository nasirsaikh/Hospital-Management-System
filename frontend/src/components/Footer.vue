<script setup></script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="left">
        <h3>Smart Hospital Management System</h3>
        <p>Providing modern digital healthcare with precision and care.</p>
      </div>

      <div class="right">
        <p>© {{ new Date().getFullYear() }} — All Rights Reserved</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #1d3557;
  color: white;
  padding: 30px 0;
  /* margin-top: 40px; */
  border-top: 2px solid #0f2238;
}

.container {
  width: 92%;
  max-width: 1200px;
  margin: auto;

  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.left h3 {
  margin: 0 0 6px;
  font-size: 18px;
  font-weight: 600;
}

.left p {
  margin: 0;
  opacity: 0.9;
}

.right p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}
</style>
