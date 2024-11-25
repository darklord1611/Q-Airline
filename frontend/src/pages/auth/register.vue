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
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  export default {
    setup() {
      // Reactive variables using ref
      const firstName = ref('');
      const lastName = ref('');
      const email = ref('');
      const password = ref('');
      const errorMessage = ref('');
  
      // Computed properties for password validation
      const passwordLength = computed(() => password.value.length >= 8);
      const passwordUppercase = computed(() => /[A-Z]/.test(password.value));
      const passwordNumber = computed(() => /\d/.test(password.value));
      const passwordSpecialChar = computed(() => /[@$!%*?&]/.test(password.value));
  
      const isPasswordStrong = computed(() => {
        return passwordLength.value && passwordUppercase.value && passwordNumber.value && passwordSpecialChar.value;
      });
  
      // Initialize the router for navigation
      const router = useRouter();
  
      // Registration handler function
      const handleRegister = async () => {
        if (!isPasswordStrong.value) {
          errorMessage.value = 'Password does not meet the required conditions. Please try again.';
          return;
        }
  
        try {
  
          // Send POST request to backend for registration
          const response = await axios.post(
            `${import.meta.env.VITE_BACKEND_URL}/auth/register`,
            {
              first_name: firstName.value,
              last_name: lastName.value,
              email: email.value,
              password: password.value,
            }
          );
  
          // Handle successful response
          console.log(response.data);
          router.push('/login'); // Redirect to login page
        } catch (error) {
          // Handle error response
          errorMessage.value = error.response?.data?.message || 'An error occurred during registration.';
        }
      };
  
      // Return everything that needs to be used in the template
      return {
        firstName,
        lastName,
        email,
        password,
        errorMessage,
        isPasswordStrong,
        handleRegister,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Add any additional styling here */
  </style>
  