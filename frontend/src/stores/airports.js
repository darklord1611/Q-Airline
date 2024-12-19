// stores/airportStore.js

import { defineStore } from 'pinia'
import apiClient from '../api/axios'

export const useAirportStore = defineStore('airportStore', {
    state: () => ({
        airports: null, // Stores the airports data
        airportsTimestamp: null, // Timestamp for cache
        cacheExpiryTime: 24 * 60 * 60 * 1000, // Cache expiry (1 day)
    }),

    actions: {
        // Fetch airports data from API and store it
        async fetchAirports() {
            try {
                // Check if we have cached data
                const cachedAirports = this.getCachedAirports()
                if (cachedAirports) {
                    return cachedAirports
                }

                // If no valid cache, fetch the data
                const response = await apiClient.get('/airports')
                const data = response.data.data // Assuming the data is in `data.data`

                // Cache the data
                this.setAirportsCache(data)

                return data
            } catch (error) {
                console.error('Error fetching airports:', error)
                throw error
            }
        },

        // Method to get cached airports data
        getCachedAirports() {
            const currentTime = new Date().getTime()
            if (this.airports && this.airportsTimestamp) {
                if (currentTime - this.airportsTimestamp < this.cacheExpiryTime) {
                    return this.airports // Return cached data if it's still valid
                } else {
                    this.clearCache() // Clear cache if expired
                }
            }
            return null
        },

        // Method to set airports data in the cache
        setAirportsCache(data) {
            this.airports = data
            this.airportsTimestamp = new Date().getTime()
        },

        // Method to clear cache
        clearCache() {
            this.airports = null
            this.airportsTimestamp = null
        },
    },
})
