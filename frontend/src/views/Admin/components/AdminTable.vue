<script setup>
defineProps({
  columns: Array,
  rows: Array
});
</script>

<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="c in columns" :key="c">{{ c }}</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="r in rows" :key="r.id">
        <td v-for="c in columns" :key="c">{{ r[c.toLowerCase()] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
}
th {
  background: #f8fafc;
  font-weight: 600;
}
</style>
