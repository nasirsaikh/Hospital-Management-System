<script setup>
import { Hand } from "lucide-vue-next";

const props = defineProps({
  name: String
});
</script>

<template>
  <div class="welcome">
    <div class="head">
      <Hand class="icon" />
      <h1>Welcome, {{ name }}</h1>
    </div>
    <p>Your health summary is ready.</p>
  </div>
</template>

<style scoped>
.welcome {
  background: linear-gradient(135deg, #457b9d, #1d3557);
  padding: 28px;
  border-radius: 16px;
  color: white;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

.head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  width: 30px;
  height: 30px;
  stroke: white;
}

h1 {
  font-size: 26px;
  font-weight: 700;
}

p {
  opacity: 0.9;
  margin-top: 4px;
}
</style>
