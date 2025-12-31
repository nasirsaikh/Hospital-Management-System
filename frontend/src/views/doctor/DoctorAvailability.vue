<script setup>
import { ref, onMounted } from "vue";
import availabilityAPI from "@/api/doctor/availability";

const loading = ref(true);
const days = ref([]);
const error = ref("");


const weekday = (iso) => {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", { weekday: "short" });
};


const formatDate = (iso) =>
  new Date(iso + "T00:00:00").toLocaleDateString("en-GB");



const snapTo30 = (val) => {
  if (!val) return null;

  const [h, m] = val.split(":").map(Number);
  const total = h * 60 + m;

  const snapped = Math.round(total / 30) * 30;

  const hh = String(Math.floor(snapped / 60)).padStart(2, "0");
  const mm = String(snapped % 60).padStart(2, "0");

  return `${hh}:${mm}`;
};


const normalizeSlot = (slotType, start, end) => {
  if (!start || !end) return { start, end };

  const s = snapTo30(start);
  const e = snapTo30(end);


  if (slotType === "morning") {
    return {
      start: s < "08:00" ? "08:00" : s,
      end: e > "12:00" ? "12:00" : e,
    };
  }

  return {
    start: s < "14:00" ? "14:00" : s,
    end: e > "20:00" ? "20:00" : e,
  };
};


const fetchAvailability = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await availabilityAPI.getAll();


    days.value = res.data;
  } catch (e) {
    error.value = "Failed to load availability.";
    days.value = [];
  }

  loading.value = false;
};



const saveSlot = async (day, slotType) => {
  const slot = day[slotType];


  const normalized = normalizeSlot(slotType, slot.start_time, slot.end_time);
  slot.start_time = normalized.start;
  slot.end_time = normalized.end;

  const payload = {
    date: day.date,
    slot_type: slotType,
    is_available: slot.is_available,
    start_time: slot.start_time,
    end_time: slot.end_time,
  };

  await availabilityAPI.save(payload);
  await fetchAvailability();
};



const toggleSlot = async (day, slotType) => {
  const slot = day[slotType];
  slot.is_available = !slot.is_available;


  if (slot.is_available && !slot.start_time) {
    if (slotType === "morning") {
      slot.start_time = "08:00";
      slot.end_time = "12:00";
    } else {
      slot.start_time = "14:00";
      slot.end_time = "20:00";
    }
  }

  await saveSlot(day, slotType);
};


onMounted(fetchAvailability);
</script>


<template>
  <div class="page">
    <h1 class="title">Availability</h1>
    <p class="subtitle">Manage your schedule for the next 7 days.</p>

    <div v-if="error" class="error">{{ error }}</div>


    <div v-if="loading" class="loader-wrap">
      <div class="loader"></div>
    </div>


    <div v-else class="days">
      <div v-for="day in days" :key="day.date" class="day-card">


        <div class="day-header">
          <div class="weekday">{{ weekday(day.date) }}</div>
          <div class="date">{{ formatDate(day.date) }}</div>
        </div>


        <div class="slot-group">


          <div class="slot-row">
            <span class="slot-label">Morning</span>

            <span class="slot-toggle" :class="{ active: day.morning.is_available }" @click="toggleSlot(day, 'morning')">
              {{ day.morning.is_available ? "Available" : "Off" }}
            </span>
          </div>

          <div v-if="day.morning.is_available" class="time-edit">
            <input type="time" v-model="day.morning.start_time" @change="saveSlot(day, 'morning')" />
            <span class="dash">–</span>
            <input type="time" v-model="day.morning.end_time" @change="saveSlot(day, 'morning')" />
          </div>


          <div class="slot-row">
            <span class="slot-label">Evening</span>

            <span class="slot-toggle" :class="{ active: day.evening.is_available }" @click="toggleSlot(day, 'evening')">
              {{ day.evening.is_available ? "Available" : "Off" }}
            </span>
          </div>

          <div v-if="day.evening.is_available" class="time-edit">
            <input type="time" v-model="day.evening.start_time" @change="saveSlot(day, 'evening')" />
            <span class="dash">–</span>
            <input type="time" v-model="day.evening.end_time" @change="saveSlot(day, 'evening')" />
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 28px;
  max-width: 650px;
  margin: auto;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #13293d;
}

.subtitle {
  margin-top: 4px;
  color: #6b7280;
  margin-bottom: 22px;
}


.days {
  display: flex;
  flex-direction: column;
  gap: 18px;
}


.day-card {
  background: white;
  padding: 18px 20px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5eaf0;
}


.day-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.weekday {
  font-size: 18px;
  font-weight: 700;
  color: #13293d;
}

.date {
  font-size: 14px;
  color: #6b7280;
}


.slot-group {
  display: flex;
  flex-direction: column;
  gap: 18px;
}


.slot-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slot-label {
  font-weight: 600;
  color: #13293d;
}


.slot-toggle {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  border: 1.8px solid #d9534f;
  background: #fee2e2;
  color: #b91c1c;
  cursor: pointer;
  transition: 0.2s;
}

.slot-toggle.active {
  border-color: #16a34a;
  background: #d1fae5;
  color: #065f46;
}


.time-edit {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: -10px;
}

.time-edit input {
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  font-size: 14px;
  outline: none;
}

.time-edit input:focus {
  border-color: #13293d;
  box-shadow: 0 0 0 2px rgba(19, 41, 61, 0.15);
}

.dash {
  font-weight: bold;
  color: #374151;
}


.loader-wrap {
  padding: 30px 0;
  display: flex;
  justify-content: center;
}

.loader {
  width: 28px;
  height: 28px;
  border: 4px solid #d1d5db;
  border-top-color: #13293d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.error {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 14px;
}
</style>
