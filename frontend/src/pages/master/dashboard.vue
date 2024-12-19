<template>
  <div class="w-full h-screen flex flex-col">
    <!-- Main content -->
    <div class="main-content w-full h-full bg-gray-50 max-w-full overflow-y-auto">
      <!-- Navbar (Hàng đầu) -->
      <div class="navbar-top w-full max-h-[150px] text-white flex items-center justify-between px-40"
        style="background: linear-gradient(135deg, #003D5B, #00577A);">
        <!-- Nội dung hàng đầu -->
        <div class="flex items-center space-x-2">
          <h3 class="font-bold text-2xl">Qairline</h3>
          <img src="@/assets/logo.png" class="w-[90px] h-[70px]" alt="Logo" />
        </div>
        <div class="flex space-x-4">
          <!-- Setting -->
          <router-link to="/setting"
            class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">
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
          <router-link to="/support"
            class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">
            <svg class="w-[20px] h-[20px] mr-2" fill="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path
                d="M2.3 2.3a2.76 2.76 0 013.9 0l1.12 1.12a2.76 2.76 0 010 3.9L6.7 8.94a.55.55 0 000 .77 11.24 11.24 0 005.6 5.6.55.55 0 00.77 0l1.62-1.62a2.76 2.76 0 013.9 0l1.12 1.12a2.76 2.76 0 010 3.9l-.9.9A3.76 3.76 0 0113.9 20a13.76 13.76 0 01-13-13A3.76 3.76 0 012.3 2.3z">
              </path>
            </svg>
            Support
          </router-link>

          <div v-if="isLoggedIn">
            <!-- User Avatar -->
            <div
              class="flex items-center py-2 px-3 space-x-4 text-sm hover:bg-gray-700 transition rounded-md cursor-pointer"
              @click="toggleDrop">
              <svg aria-hidden="true" class="w-[24px] h-[26px] mr-2 fill-current" fill="currentColor"
                viewBox="0 0 24 21" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                  clip-rule="evenodd"></path>
              </svg>
            </div>
            <!-- Drop-down -->
            <div v-show="showDropDown"
              class="absolute right-[50px] z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
              <div class="py-1 text-left" role="none">
                <router-link to="/profile" class="text-gray-700 block px-4 py-2 text-sm">Profile</router-link>
                <button @click="handleLogout" class="text-gray-700 block px-4 py-2 text-sm">Logout</button>
              </div>
            </div>
          </div>
          <div v-else class="flex items-center justify-start space-x-4">
            <!-- Login and Register Buttons -->
            <router-link to="/login"
              class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">Login</router-link>
            <router-link to="/register"
              class="flex items-center py-2 px-3 text-sm hover:bg-gray-700 transition rounded-md">Register</router-link>
          </div>
        </div>
      </div>

      <!-- Navbar (Hàng thứ hai) -->
      <div class="navbar-bottom w-full bg-white border-t border-gray-300 flex justify-between items-center px-40">
        <div class="flex w-full">
          <router-link to="/booking"
            class="flex-1 py-3 px-4 text-sm text-center border-r border-gray-300 hover:bg-gray-100 transition rounded-md">
            Booking
          </router-link>
          <router-link to="/myflight"
            class="flex-1 py-3 px-4 text-sm text-center border-r border-gray-300 hover:bg-gray-100 transition rounded-md flex items-center justify-center">
            <!-- Nội dung My Flight -->
            <span>My Flight</span>

            <!-- Hiển thị icon chuông nếu isDelay = true -->
            <img v-if="isNotified" src="@/assets/bell-icon.png" alt="Delay Icon"
              class="w-4 h-4 ml-2 img-bell bell-animation" />
          </router-link>
          <router-link to="/flightSchedule"
            class="flex-1 py-3 px-4 text-sm text-center hover:bg-gray-100 transition rounded-md">
            Flight Schedule
          </router-link>
        </div>
      </div>

      <!-- Container chính của thông báo -->
      <div v-if="showDelayNotification" class="notification-container">

        <!-- Nội dung thông báo -->
        <div class="notification-content">
          <!-- Icon đồng hồ minh họa -->
          <img src="@/assets/clock-icon.png" alt="Clock Icon" class="notification-icon" />

          <!-- Nội dung chuyến bay delay -->
          <p class="notification-title">
            Your flight has been <span class="text-red">delayed</span>
          </p>
          <p class="notification-time">
            New departure time: <span class="bold-text">18h30</span>
          </p>
        </div>

        <!-- Nút Get It! -->
        <button @click="handleGetIt" class="notification-button">
          Get It!
        </button>
      </div>

      <div v-if="showSuccessNotification" class="notification-container">
        <!-- Nội dung thông báo -->
        <div class="notification-content">
          <!-- Icon minh họa -->
          <img src="@/assets/success-icon.png" alt="Success Icon" class="notification-icon" />

          <!-- Nội dung đặt vé thành công -->
          <p class="notification-title">
            Your ticket has been <span class="text-green">successfully booked!</span>
          </p>
          <p class="notification-details">
            Booking reference: <span class="bold-text">ABC123XYZ</span>
          </p>
        </div>

        <!-- Nút OK -->
        <button @click="handleOk" class="notification-button">
          Get It!
        </button>
      </div>

      <!-- Nội dung chính -->
      <div class="w-full content">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </div>
    </div>
  </div>
</template>


<script>
import { useUserStore } from '@/stores/user';
import login from "@/pages/auth/login.vue";
import apiClient from '@/api/axios';

export default {
  components: {
    login,
  },
  data() {
    return {
      showDropDown: false,
      isNotified: true,
      userStore: useUserStore(), // Access the store in data to use it later
      notifications: [],
      showDelayNotification: false,
      showSuccessNotification: true,
    };
  },
  computed: {
    // Use computed properties to reactively get store state
    isLoggedIn() {
      return this.userStore.isLoggedIn;
    },
    user() {
      return this.userStore.user;
    },
  },
  async created() {
    // Any setup logic you want to run when the component is created
    console.log("User data on created:", this.user);

    // fetch notifications

    const response = await apiClient.get(`/notifications/${this.user.id}`);


    this.notifications = response.data.data;

    console.log("Notifications:", this.notifications);
  },
  methods: {
    // Toggles the dropdown state
    toggleDrop() {
      this.showDropDown = !this.showDropDown;
    },
    // Handles user logout by calling the store logout method
    handleLogout() {
      this.userStore.logout();
      this.$router.push("/login");
    },
    handleGetIt() {
      this.showDelayNotification = false;
      this.isNotified = false;
    },
    handleOk() {
      this.showSuccessNotification = false;
      this.isNotified = false;
    },
  },
};
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

.img-bell {
  display: inline-block;
}

@keyframes bell-shake {
  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(-10deg);
  }

  50% {
    transform: rotate(10deg);
  }

  75% {
    transform: rotate(-5deg);
  }

  100% {
    transform: rotate(0deg);
  }
}

.bell-animation {
  display: inline-block;
  animation: bell-shake 0.5s ease-in-out infinite;
}

.notification-container {
  background-color: #ffffff;
  width: 100%;
  max-height: 300px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  overflow: hidden;
}


/* Nội dung thông báo */
.notification-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  background-color: #f0f7ff;
  width: 100%;
  text-align: center;
}

/* Icon đồng hồ */
.notification-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

/* Tiêu đề thông báo */
.notification-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

/* Nội dung giờ khởi hành */
.notification-time {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Văn bản màu đỏ */
.text-red {
  color: #e63946;
}

/* Chữ in đậm */
.bold-text {
  font-weight: bold;
}

/* Nút "Get It!" */
.notification-button {
  width: 100%;
  padding: 12px 0;
  background: linear-gradient(135deg, #00A8E8, #4FC3F7);
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.notification-button:hover {
  opacity: 0.9;
}

.notification-details {
  font-size: 0.95rem;
  color: #555555;
  margin-top: 5px;
}
</style>
