<template>
  <div class="w-full h-screen flex flex-col">
    <!-- Navbar (Hàng đầu) -->
    <div class="w-full max-h-[200px]  text-white flex items-center justify-between px-40 max-w-full mx-auto"
      style="background-color: #003D5B;">
      <!-- Menu Items -->
      <div class="flex items-center space-x-2">
        <h3 class="font-bold text-2xl">Qairline</h3>
        <img src="@/assets/logo.png" class="w-[90px] h-[80px]" alt="Logo" />
      </div>
      <!-- Setting, Support, Login/Logout -->
      <div class="flex space-x-4">
        <!-- Setting -->
        <router-link to="/setting" class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">
          <svg class="w-[20px] h-[20px] mr-2" fill="currentColor" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path d="M12 8.5a3.5 3.5 0 110 7 3.5 3.5 0 010-7z"></path>
            <path fill-rule="evenodd"
              d="M12 2a1 1 0 01.995.9l.257 2.047a8.034 8.034 0 013.02 1.258l1.803-.777a1 1 0 011.29.297l1.5 2.598a1 1 0 01-.234 1.29l-1.686 1.277a8.06 8.06 0 01-.002 2.515l1.688 1.278a1 1 0 01.233 1.29l-1.5 2.598a1 1 0 01-1.29.297l-1.803-.777a8.034 8.034 0 01-3.02 1.258l-.257 2.047a1 1 0 01-1.99 0l-.257-2.047a8.034 8.034 0 01-3.02-1.258l-1.803.777a1 1 0 01-1.29-.297l-1.5-2.598a1 1 0 01.233-1.29l1.688-1.278a8.06 8.06 0 01-.002-2.515L2.593 9.613a1 1 0 01-.233-1.29l1.5-2.598a1 1 0 011.29-.297l1.803.777A8.034 8.034 0 0111 4.947l.257-2.047A1 1 0 0112 2zm-4.5 10a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0z"
              clip-rule="evenodd"></path>
          </svg>
          Setting
        </router-link>

        <!-- Support -->
        <router-link to="/support" class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">
          <svg class="w-[20px] h-[20px] mr-2" fill="currentColor" viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg">
            <path
              d="M2.3 2.3a2.76 2.76 0 013.9 0l1.12 1.12a2.76 2.76 0 010 3.9L6.7 8.94a.55.55 0 000 .77 11.24 11.24 0 005.6 5.6.55.55 0 00.77 0l1.62-1.62a2.76 2.76 0 013.9 0l1.12 1.12a2.76 2.76 0 010 3.9l-.9.9A3.76 3.76 0 0113.9 20a13.76 13.76 0 01-13-13A3.76 3.76 0 012.3 2.3z">
            </path>
          </svg>
          Support
        </router-link>
        
        <div v-if="isLoggedIn">
            <!-- User Avatar -->
            <div class="flex items-center justify-start space-x-4" @click="toggleDrop">
              <svg aria-hidden="true" class="mr-2 w-[25px] h-[25px] fill-current" fill="currentColor" viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                  clip-rule="evenodd"></path>
              </svg>
            </div>
            <!-- Drop-down -->
            <div v-show="showDropDown"
              class="absolute right-[10px] z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
              <div class="py-1 text-left" role="none">
                <router-link to="/profile" class="text-gray-700 block px-4 py-2 text-sm">Profile</router-link>
                <button @click="handleLogout" class="text-gray-700 block px-4 py-2 text-sm">Logout</button>
              </div>
            </div>
          </div>
          <div v-else class="flex items-center justify-start space-x-4">
            <!-- Login and Register Buttons -->
            <router-link to="/login" class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">Login</router-link>
            <router-link to="/register" class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">Register</router-link>
          </div>
      </div>
    </div>

    <!-- Navbar (Hàng thứ hai) -->
    <div class="w-full bg-white border-t border-gray-300 flex justify-between items-center px-40 max-w-full mx-auto">
      <div class="flex w-full">
        <!-- Booking -->
        <router-link to="/booking"
          class="flex-1 py-3 px-4 text-sm text-center border-r border-gray-300 hover:bg-gray-100 transition rounded-md font">
          Booking
        </router-link>

        <!-- My Flight -->
        <router-link to="/myflight"
          class="flex-1 py-3 px-4 text-sm text-center border-r border-gray-300 hover:bg-gray-100 transition rounded-md font">
          My Flight
        </router-link>

        <!-- Flight Schedule -->
        <router-link to="/flightSchedule"
          class="flex-1 py-3 px-4 text-sm text-center hover:bg-gray-100 transition rounded-md font">
          Flight Schedule
        </router-link>
      </div>
    </div>

    <!-- Main content -->
    <div class="main-content w-full h-full bg-gray-50 max-w-full">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import login from "@/pages/auth/login.vue";
import { computed } from 'vue';

export default {
  components: {
    login,
  },
  data() {
    return {
      showDropDown: false,
    };
  },
  methods: {
    toggleDrop() {
      this.showDropDown = !this.showDropDown

    }
  },
  setup() {
    const userStore = useUserStore();

    // Use computed properties to ensure the dashboard re-renders when the store state changes
    const isLoggedIn = computed(() => userStore.isLoggedIn);
    const user = computed(() => userStore.user);

    // Handle logout by calling the logout method from the store
    const handleLogout = () => {
      userStore.logout();
    };

    return {
      isLoggedIn,
      user,
      handleLogout,
    };
  },


}

</script>



<style scoped>
/* Đảm bảo không có tràn màn hình */
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.w-full.h-screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Đảm bảo chiều cao tối thiểu là bằng chiều cao của màn hình */
}

.main-content {
  flex: 1;
  /* Chiếm toàn bộ không gian còn lại */
  overflow-y: auto;
  /* Thêm thanh cuộn nếu nội dung dài */
}

.font {
  font-family: 'Merriweather', serif;
  font-weight: bold;
}
</style>
