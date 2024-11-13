<!-- frontend/pages/fetch-flight.vue -->
<template>
  <div>
    <h1>Flight Information</h1>
    <button @click="fetchAirports">Fetch Airports</button>

    <div v-if="loading">Loading...</div>
    
    <ul v-if="airports.length && !loading">
      <li v-for="airport in airports" :key="airport.id">
        {{ airport.name }} - {{ airport.city }}
      </li>
    </ul>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      airports: [],
      loading: false,
      error: null,
    }
  },
  methods: {
    async fetchAirports() {
      this.loading = true
      this.error = null
      try {
        // Adjust the URL to match your FastAPI server address
        const { data } = await axios.get("https://8000-01jbhjyh5b1bap55ffv7xg7wq4.cloudspaces.litng.ai/api/v1/airports")
        this.airports = data.data
      } catch (err) {
        this.error = "Failed to load flights"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
