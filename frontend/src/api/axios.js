import axios from 'axios';
import { useUserStore } from '@/stores/user'; // Adjust path as needed

// Create an instance of axios
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL || 'https://your-api.com', // Replace with your API base URL
    timeout: 60000, // Set a timeout in milliseconds
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to append the access token
apiClient.interceptors.request.use(
    (config) => {
        const userStore = useUserStore(); // Access your user store

        // If the user is logged in, add the Authorization header
        if (userStore.isLoggedIn && userStore.accessToken) {
            config.headers.Authorization = `Bearer ${userStore.accessToken}`;
        }

        return config;
    },
    (error) => {
        // Handle errors before the request is sent
        return Promise.reject(error);
    }
);

export default apiClient;
