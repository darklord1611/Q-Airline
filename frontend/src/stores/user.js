import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore(
    'user',
    () => {
        // State
        const isLoggedIn = ref(false);
        const isAdmin = ref(false);
        const user = ref(null);
        const accessToken = ref("");
        const refreshToken = ref("");

        // Set user after login
        const setUser = (userData, userAccessToken, userRefreshToken) => {
            isLoggedIn.value = true;
            user.value = userData;
            if (userData.role === 'admin') {
                isAdmin.value = true;
            }
            accessToken.value = userAccessToken;
            refreshToken.value = userRefreshToken;
        };

        // Logout functionality
        const logout = () => {
            isLoggedIn.value = false;
            isAdmin.value = false;
            user.value = null;
            accessToken.value = "";
            refreshToken.value = "";
        };

        // Return all states and methods
        return {
            isLoggedIn,
            isAdmin,
            user,
            accessToken,
            refreshToken,
            setUser,
            logout,
        };
    },
    {
        persist: {
            key: 'user-store', // Custom key in localStorage
            storage: window.localStorage, // Use localStorage (default)
            paths: ['isLoggedIn', 'user', 'accessToken', 'refreshToken'], // Specify the fields to persist
        },
    }
);
