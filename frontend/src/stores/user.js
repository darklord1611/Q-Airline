// store/user.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
    const isLoggedIn = ref(false); // State to track if the user is logged in
    const user = ref(null); // Store user details after login
    const accessToken = ref(""); // Store the access token after login
    const refreshToken = ref(""); // Store the refresh token after login

    const setUser = (userData, userAccessToken, userRefreshToken) => {
        isLoggedIn.value = true;
        user.value = userData; // Set the user data after successful login
        accessToken.value = userAccessToken; // Set the access token after successful login
        refreshToken.value = userRefreshToken; // Set the refresh token after successful login
    };

    const logout = () => {
        isLoggedIn.value = false;
        user.value = null; // Clear the user data when logged out
    };

    return {
        isLoggedIn,
        user,
        setUser,
        logout,
    };
}, {
    persist: true // This will persist the store state in localStorage or sessionStorage
});
