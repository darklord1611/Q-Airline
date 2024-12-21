// stores/bookingsStore.js
import { defineStore } from "pinia";
import apiClient from "@/api/axios"; // Adjust the path as needed

const CACHE_KEY = "bookingsCache";
const CACHE_METADATA_KEY = "bookingsMetadata";

export const useBookingStore = defineStore("bookingsStore", {
    state: () => ({
        bookings: [], // Holds the list of bookings
        cacheTimeout: 15 * 60 * 1000, // Cache expiration time in milliseconds (default: 15 minutes)
    }),
    actions: {
        // check if the data is cached
        isCached() {
            const cachedBookings = localStorage.getItem(CACHE_KEY);
            const cacheMetadata = JSON.parse(localStorage.getItem(CACHE_METADATA_KEY) || "{}");

            if (cachedBookings && cacheMetadata.lastUpdated) {
                const currentTime = Date.now();
                const isCacheValid = currentTime - cacheMetadata.lastUpdated < this.cacheTimeout;

                if (isCacheValid) {
                    return true;
                } else {
                    return false;
                }
            }
            return false;
        },
        async fetchBookings(userId) {
            // const currentTime = Date.now();

            // // Check if bookings are already cached
            // const cachedBookings = localStorage.getItem(CACHE_KEY);
            // const cacheMetadata = JSON.parse(localStorage.getItem(CACHE_METADATA_KEY) || "{}");

            // if (cachedBookings && cacheMetadata.lastUpdated) {
            //     const isCacheValid = currentTime - cacheMetadata.lastUpdated < this.cacheTimeout;

            //     if (isCacheValid) {
            //         console.log("Using cached bookings data");
            //         this.bookings = JSON.parse(cachedBookings);
            //         return this.bookings;
            //     } else {
            //         console.log("Cache expired. Fetching fresh data...");
            //         this.clearCache();
            //     }
            // }

            try {
                console.log("Fetching bookings data from API");
                // Fetch bookings from the API
                const response = await apiClient.get(`/bookings?user_id=${userId}`);
                const bookingsData = response.data.data;

                console.log(bookingsData);

                // Process bookings data
                const processedBookings = bookingsData.map((booking) => ({
                    ...booking,
                    totalMeal: this.calcTotalMeal(booking.flights[0].services),
                    totalLuggage: this.calcTotalLuggage(booking.flights[0].services),
                    formattedCheckIn: this.formatDate(booking.flights[0].checkin),
                    formattedCheckOut: this.formatDate(booking.flights[0].checkout),
                }));

                // Update the store state
                this.bookings = processedBookings;

                // Cache the processed bookings in localStorage
                localStorage.setItem(CACHE_KEY, JSON.stringify(processedBookings));
                localStorage.setItem(
                    CACHE_METADATA_KEY,
                    JSON.stringify({ lastUpdated: currentTime })
                );
                return this.bookings;
            } catch (error) {
                console.error("Error fetching bookings data:", error);
            }
        },
        clearCache() {
            // Clears the cached bookings
            localStorage.removeItem(CACHE_KEY);
            localStorage.removeItem(CACHE_METADATA_KEY);
            this.bookings = [];
        },
        setCacheTimeout(timeout) {
            // Allows dynamic updating of the cache timeout
            this.cacheTimeout = timeout;
        },

        // Add a new booking to the cache
        addBookingToCache(newBooking) {
            // Check if the booking already exists in the cache
            const existingBookingIndex = this.bookings.findIndex(
                (booking) => booking.id === newBooking.id
            );

            if (existingBookingIndex !== -1) {
                console.log(`Booking with ID ${newBooking.id} already exists in the cache.`);
                return;
            }

            // Process the new booking data
            const processedBooking = {
                ...newBooking,
                totalMeal: this.calcTotalMeal(newBooking.flights[0].services),
                totalLuggage: this.calcTotalLuggage(newBooking.flights[0].services),
                formattedCheckIn: this.formatDate(newBooking.flights[0].checkin),
                formattedCheckOut: this.formatDate(newBooking.flights[0].checkout),
            };

            // Add the new booking to the store and update the cached data
            this.bookings.push(processedBooking);
            const currentTime = Date.now();

            // Update the cache with the new booking data
            localStorage.setItem(CACHE_KEY, JSON.stringify(this.bookings));
            localStorage.setItem(
                CACHE_METADATA_KEY,
                JSON.stringify({ lastUpdated: currentTime })
            );
            console.log(`Booking with ID ${newBooking.id} added to the cache.`);
        },

        // Remove a specific booking from the cache by ID
        removeBookingFromCache(bookingId) {
            // Find and remove the booking with the given ID
            const index = this.bookings.findIndex((booking) => booking.id === bookingId);
            if (index !== -1) {
                this.bookings.splice(index, 1);
                console.log(`Booking with ID ${bookingId} removed from the cache.`);

                // Update the cached data
                const currentTime = Date.now();
                localStorage.setItem(CACHE_KEY, JSON.stringify(this.bookings));
                localStorage.setItem(
                    CACHE_METADATA_KEY,
                    JSON.stringify({ lastUpdated: currentTime })
                );
            } else {
                console.log(`Booking with ID ${bookingId} not found in the cache.`);
            }
        },

        calcTotalMeal(services) {
            return services.reduce((total, service) => {
                if (service.services.type === "MEAL") {
                    total += service.quantity;
                }
                return total;
            }, 0);
        },

        calcTotalLuggage(services) {
            return services.reduce((total, service) => {
                if (service.services.type === "LUGGAGE") {
                    total += service.quantity;
                }
                return total;
            }, 0);
        },

        formatDate(inputDate) {
            // Convert date to a formatted string
            const date = new Date(inputDate);
            const options = { weekday: "short", day: "numeric", month: "short" };
            return date.toLocaleDateString("en-US", options);
        },
    },
});
