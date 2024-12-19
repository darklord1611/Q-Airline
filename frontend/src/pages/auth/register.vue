<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold text-center mb-6">Register</h2>
  
        <form @submit.prevent="handleRegister">
          <!-- First Name -->
          <div class="mb-4">
            <input
              v-model="firstName"
              type="text"
              id="firstName"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300"
              placeholder="First Name"
              required
            />
          </div>
  
          <!-- Last Name -->
          <div class="mb-4">
            <input
              v-model="lastName"
              type="text"
              id="lastName"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300"
              placeholder="Last Name"
              required
            />
          </div>
  
          <!-- Email -->
          <div class="mb-4">
            <input
              v-model="email"
              type="email"
              id="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300"
              placeholder="Email"
              required
            />
          </div>
  
          <!-- Password -->
          <div class="mb-4">
            <input
              v-model="password"
              type="password"
              id="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-300"
              placeholder="Password"
              required
            />
            <ul class="text-sm text-gray-500 mt-2 space-y-1">
              <li :class="{ 'text-green-600': passwordLength }">
                ✔ At least 8 characters
              </li>
              <li :class="{ 'text-green-600': passwordUppercase }">
                ✔ At least one uppercase letter
              </li>
              <li :class="{ 'text-green-600': passwordNumber }">
                ✔ At least one number
              </li>
              <li :class="{ 'text-green-600': passwordSpecialChar }">
                ✔ At least one special character
              </li>
            </ul>
          </div>
  
          <!-- Error Message -->
          <p v-if="errorMessage" class="text-red-500 text-sm mb-4">{{ errorMessage }}</p>
  
          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  </template>
  
<script>

import apiClient from '@/api/axios';

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
    };
  },
  computed: {
    // Computed properties for password validation
    passwordLength() {
      return this.password.length >= 8;
    },
    passwordUppercase() {
      return /[A-Z]/.test(this.password);
    },
    passwordNumber() {
      return /\d/.test(this.password);
    },
    passwordSpecialChar() {
      return /[@$!%*?&]/.test(this.password);
    },
    isPasswordStrong() {
      return (
        this.passwordLength &&
        this.passwordUppercase &&
        this.passwordNumber &&
        this.passwordSpecialChar
      );
    },
  },
  methods: {
    // Registration handler function
    async handleRegister() {
      if (!this.isPasswordStrong) {
        this.$toastr.error('Password does not meet the required conditions. Please try again.');
      }

      try {
        // Send POST request to backend for registration
        const payload = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          password: this.password,
        };

        const response = await apiClient.post('/auth/register', payload);

        // Handle successful response
        console.log(response.data.data);
        this.$toastr.success("Register successfully!. Redirecting to login page...");
        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);
      } catch (error) {
        // Handle error response
        console.log(error)
        this.$toastr.error('An error occurred during registration.');
      }
    },
  },
  created() {
    // Example: Perform any setup tasks, like fetching initial data
    console.log('Component created, ready for user input.');
  },
};
</script>
  

<style scoped>
/* Add any additional styling here */
</style>
  