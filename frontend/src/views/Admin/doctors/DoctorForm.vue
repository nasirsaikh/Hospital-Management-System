<script setup>
import { ref, onMounted } from "vue";
import adminDoctorsAPI from "@/api/admin/doctors";

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  editMode: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(["update:modelValue", "submit"]);

const specializations = ref([]);
const specsError = ref("");

const loadSpecs = async () => {
  try {
    const res = await adminDoctorsAPI.getSpecializations();
    specializations.value = res.data || [];
  } catch (e) {
    console.error("Failed to load specializations", e);
    specsError.value = "Unable to load specializations";
  }
};
onMounted(loadSpecs);

const numericFields = ["age", "experience_years", "specialization_id", "consultation_fee"];

const updateField = (field, value) => {
  let cleaned = value;

  if (numericFields.includes(field)) {
    if (value === "" || value === null) cleaned = null;
    else {
      const n = Number(value);
      cleaned = Number.isNaN(n) ? null : n;
    }
  }

  emit("update:modelValue", { ...props.modelValue, [field]: cleaned });
};
</script>

<template>
  <div class="form-card">

    <h2 class="form-title">
      {{ editMode ? "Edit Doctor Profile" : "Create New Doctor" }}
    </h2>

    <div class="form-grid">


      <div class="field">
        <label>Full Name</label>
        <input :value="modelValue.full_name || ''" @input="updateField('full_name', $event.target.value)"
          placeholder="Doctor full name" />
      </div>


      <div class="field">
        <label>Email</label>
        <input :value="modelValue.email || ''" @input="updateField('email', $event.target.value)"
          placeholder="Email address" :disabled="editMode" />
      </div>


      <div class="field" v-if="!editMode">
        <label>Password</label>
        <input type="password" :value="modelValue.password || ''" @input="updateField('password', $event.target.value)"
          placeholder="Account password" />
      </div>


      <div class="field">
        <label>Phone</label>
        <input :value="modelValue.phone || ''" @input="updateField('phone', $event.target.value)"
          placeholder="Phone number" />
      </div>


      <div class="field">
        <label>Age</label>
        <input type="number" :value="modelValue.age ?? ''" @input="updateField('age', $event.target.value)"
          placeholder="Age" />
      </div>


      <div class="field">
        <label>Gender</label>
        <select :value="modelValue.gender || ''" @change="updateField('gender', $event.target.value)">
          <option disabled value="">Select gender</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>


      <div class="field full">
        <label>Specialization</label>
        <select :value="modelValue.specialization_id ?? ''"
          @change="updateField('specialization_id', $event.target.value)">
          <option disabled value="">Select Department</option>
          <option v-for="s in specializations" :key="s.id" :value="s.id">
            {{ s.name }}
          </option>
        </select>
        <div v-if="specsError" class="error">{{ specsError }}</div>
      </div>


      <div class="field full">
        <label>Qualification</label>
        <input :value="modelValue.qualification || ''" @input="updateField('qualification', $event.target.value)"
          placeholder="MBBS, MD, etc." />
      </div>


      <div class="field">
        <label>Experience</label>
        <input type="number" :value="modelValue.experience_years ?? ''"
          @input="updateField('experience_years', $event.target.value)" placeholder="Years of experience" />
      </div>


      <div class="field">
        <label>Consultation Fee</label>
        <input type="number" :value="modelValue.consultation_fee ?? ''"
          @input="updateField('consultation_fee', $event.target.value)" placeholder="Fee in ₹" />
      </div>


      <div class="field full">
        <label>Short Bio</label>
        <textarea rows="3" :value="modelValue.bio || ''" @input="updateField('bio', $event.target.value)"
          placeholder="Brief introduction about the doctor"></textarea>
      </div>

    </div>

    <button class="submit-btn" :disabled="props.loading" @click="$emit('submit')">
      {{ props.loading ? "Saving..." : editMode ? "Save Changes" : "Create Doctor" }}
    </button>

  </div>
</template>

<style scoped>
.form-card {
  background: white;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  max-width: 900px;
  margin: auto;
}


.form-title {
  font-size: 22px;
  color: #1d3557;
  font-weight: 700;
  margin-bottom: 20px;
  text-align: center;
}


.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}


.field {
  display: flex;
  flex-direction: column;
}

.field.full {
  grid-column: span 2;
}

label {
  font-size: 14px;
  margin-bottom: 6px;
  color: #374151;
}

input,
select,
textarea {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f9fafb;
  font-size: 14px;
  transition: 0.2s border, 0.2s box-shadow;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #1d3557;
  box-shadow: 0 0 0 2px rgba(29, 53, 87, 0.2);
}


.error {
  margin-top: 4px;
  font-size: 13px;
  color: #dc2626;
}


.submit-btn {
  margin-top: 26px;
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #1d3557, #457b9d);
  color: white;
  border-radius: 10px;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: 0.2s;
}

.submit-btn:hover:not([disabled]) {
  opacity: 0.92;
  transform: translateY(-1px);
}

.submit-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
