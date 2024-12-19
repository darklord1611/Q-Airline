<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
      <h2 class="text-2xl font-semibold text-center mb-6">Login</h2>

      <form @submit.prevent="handleSubmit">
        <!-- Email Field -->
        <div class="mb-4">
          <input v-model="email" type="email" id="email" placeholder="Enter your email"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300 focus:outline-none"
            required />
        </div>

        <!-- Password Field -->
        <div class="mb-4">
          <input v-model="password" type="password" id="password" placeholder="Enter your password"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300 focus:outline-none"
            required />
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-500 text-sm mb-4">{{ errorMessage }}</p>

        <!-- Submit Button -->
        <div class="mt-6">
          <button type="submit"
            class="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-300">
            Login
          </button>
        </div>

        <!-- Register Link -->
        <p class="mt-4 text-center">
          Don't have an account? <router-link to="/register" class="text-blue-500">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      email: "",  // Email input
      password: "",  // Password input
      errorMessage: "",  // Error message
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/auth/login`, {
          email: this.email,
          password: this.password,
        });

        console.log(response.data);

        // Assuming response includes { token, user }
        const { access_token, refresh_token, user } = response.data;

        // Store user info in Pinia
        const userStore = useUserStore();
        userStore.setUser(user, access_token, refresh_token);

        // Show success message
        this.$toastr.success("Login successful! Redirecting...");

        // Redirect after a short delay
        setTimeout(() => {
          this.$router.push("/booking");
        }, 1000);
      } catch (error) {
        console.error(error);
        this.$toastr.error("Login failed! Please try again.");
      }
    },
  },
};
</script>
