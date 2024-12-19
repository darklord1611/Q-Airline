import { defineStore } from "pinia";
import apiClient from "@/api/axios"; // Adjust the path as needed

const CACHE_KEY = "flightAnalyticsCache";
const CACHE_METADATA_KEY = "flightAnalyticsMetadata";

export const useFlightAnalyticStore = defineStore("flightAnalyticsStore", {
    state: () => ({
        flightAnalytics: [], // Holds the ticket counts and revenues from each flight
        cacheTimeout: 15 * 60 * 1000, // Cache expiration time in milliseconds (default: 15 minutes)
    }),
    actions: {
        async fetchFlightAnalytics() {
            const currentTime = Date.now();

            // Check if flight analytics are already cached
            const cachedAnalytics = localStorage.getItem(CACHE_KEY);
            const cacheMetadata = JSON.parse(localStorage.getItem(CACHE_METADATA_KEY) || "{}");

            if (cachedAnalytics && cacheMetadata.lastUpdated) {
                const isCacheValid = currentTime - cacheMetadata.lastUpdated < this.cacheTimeout;

                if (isCacheValid) {
                    console.log("Using cached flight analytics data");
                    this.flightAnalytics = JSON.parse(cachedAnalytics);
                    return this.flightAnalytics;
                } else {
                    console.log("Cache expired. Fetching fresh data...");
                    this.clearCache();
                }
            }

            try {
                console.log("Fetching flight analytics data from API");
                // Fetch flight data from the API
                const response = await apiClient.get("/flights/analytics/all");
                const analyticsData = response.data.data;

                console.log(analyticsData)

                // Process and map the flight data
                const processedAnalytics = analyticsData.map((flight) => {
                    let economyTickets = 0;
                    let businessTickets = 0;
                    let economyRevenue = 0;
                    let businessRevenue = 0;

                    flight.services.forEach((service) => {
                        if (service.name === "ECONOMY") {
                            economyTickets = service.count || 0;
                            economyRevenue = service.revenue || 0;
                        } else if (service.name === "BUSINESS") {
                            businessTickets = service.count || 0;
                            businessRevenue = service.revenue || 0;
                        }
                    });

                    return {
                        flightId: flight.flight_id,
                        flightNumber: flight.flight_number,
                        economyTickets,
                        businessTickets,
                        economyRevenue,
                        businessRevenue,
                    };
                });

                // Update the store state
                this.flightAnalytics = processedAnalytics;

                // Cache the processed analytics in localStorage
                localStorage.setItem(CACHE_KEY, JSON.stringify(processedAnalytics));
                localStorage.setItem(
                    CACHE_METADATA_KEY,
                    JSON.stringify({ lastUpdated: currentTime })
                );
                return this.flightAnalytics;
            } catch (error) {
                console.error("Error fetching flight analytics data:", error);
            }
        },
        clearCache() {
            // Clears the cached flight analytics
            localStorage.removeItem(CACHE_KEY);
            localStorage.removeItem(CACHE_METADATA_KEY);
            this.flightAnalytics = [];
        },
        setCacheTimeout(timeout) {
            // Allows dynamic updating of the cache timeout
            this.cacheTimeout = timeout;
        },

        // Add new flight to the cached data
        addFlightToCache(newFlight) {
            // First, check if the flight already exists in the cache
            const existingFlightIndex = this.flightAnalytics.findIndex(
                (flight) => flight.flightId === newFlight.flight_id
            );

            if (existingFlightIndex !== -1) {
                console.log(`Flight with ID ${newFlight.flight_id} already exists in the cache.`);
                return;
            }

            // Process the new flight data as per the structure of cached data
            const processedFlight = {
                flightId: newFlight.flight_id,
                flightNumber: newFlight.flight_number,
                economyTickets: newFlight.services.find((s) => s.name === "ECONOMY")?.count || 0,
                businessTickets: newFlight.services.find((s) => s.name === "BUSINESS")?.count || 0,
                economyRevenue: newFlight.services.find((s) => s.name === "ECONOMY")?.revenue || 0,
                businessRevenue: newFlight.services.find((s) => s.name === "BUSINESS")?.revenue || 0,
            };

            // Add the new flight to the store and update the cached data
            this.flightAnalytics.push(processedFlight);
            const currentTime = Date.now();

            // Update the cache with the new flight data
            localStorage.setItem(CACHE_KEY, JSON.stringify(this.flightAnalytics));
            localStorage.setItem(
                CACHE_METADATA_KEY,
                JSON.stringify({ lastUpdated: currentTime })
            );
            console.log(`Flight with ID ${newFlight.flight_id} added to the cache.`);
        },
    },
});
