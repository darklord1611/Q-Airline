<template>
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
                {{ latest_notification.description }}
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
                {{ latest_notification.description }}
            </p>
        </div>

        <!-- Nút OK -->
        <button @click="handleOk" class="notification-button">
            Get It!
        </button>
    </div>

    <AdminPost />

    <div class="myflight-profile">
        <div class="flight-list">
            <div class="search-bar">
                <img src="@/assets/search.png" alt="Search Icon" class="icon" />
                <input type="text" class="search-input" placeholder="Find your ticket by arrival city"
                    v-model="searchQuery" />
            </div>
            <div class="flight-card" v-for="booking in filteredBookings" :key="booking.id">
                <div class="flight-info-horizontal">
                    <!-- Cột trái: Thời gian -->
                    <div class="time-column">
                        <div class="time-block departure-time">
                            <span class="time">{{ booking.flights[0].departure_time }}</span>
                            <div class="date">{{ booking.formattedCheckIn }}</div>
                        </div>
                        <div class="spacer"></div>
                        <div class="duration"><span>{{ booking.flights[0].duration }}</span></div>
                        <div class="time-block arrival-time">
                            <span class="time">{{ booking.flights[0].arrival_time }}</span>
                            <div class="date">{{ booking.formattedCheckOut }}</div>
                        </div>
                    </div>

                    <!-- Cột giữa: Đường bay -->
                    <div class="route-column">
                        <div class="icon icon-departure">●</div>
                        <div class="line"></div>
                        <div class="icon icon-plane">
                            <img src="@/assets/plane.png" alt="plane icon" />
                        </div>
                        <div class="line"></div>
                        <div class="icon icon-location">
                            <img src="@/assets/location-sign.png" alt="location icon" />
                        </div>
                    </div>

                    <!-- Cột phải: Sân bay -->
                    <div class="airport-column">
                        <div class="airport-block departure-airport">
                            <span>{{ booking.flights[0].departure_iata_code }}</span>
                            <div class="from"> {{ booking.flights[0].departure_city }}</div>
                        </div>
                        <div class="service">
                            <!-- Phần Hành lý -->
                            <div class="luggage">
                                <img src="@/assets/luggage.png" alt="Luggage Icon" class="service-icon" />
                                <span class="service-text">{{ booking.totalLuggage }} kg</span>
                            </div>

                            <!-- Phần Bữa ăn -->
                            <div class="meal">
                                <img src="@/assets/breakfast.png" alt="Meal Icon" class="service-icon" />
                                <span class="service-text">{{ booking.totalMeal }} meals</span>
                            </div>
                            <div class="travelers">
                                <img src="@/assets/passenger.png" alt="passerger Icon" class="service-icon" />
                                <span class="service-text">{{ booking.number_of_passengers }} passengers</span>
                            </div>
                        </div>

                        <div class="airport-block arrival-airport">
                            <span>{{ booking.flights[0].arrival_iata_code }}</span>
                            <div class="from"> {{ booking.flights[0].arrival_city }}</div>
                        </div>
                    </div>

                </div>


                <!-- Thông tin giá và nút chọn -->
                <div class="price-info-horizontal">
                    <span class="price">USD: {{ booking.total_price }}$</span>
                    <span class="ticket"> {{ booking.class_name }}</span>
                    <button v-if="shouldRenderCancelButton(booking)" class="cancel-button"
                        @click="removeFlight(booking.id)">Cancel</button>
                </div>
            </div>
        </div>
        <div class="profile-weather">
            <Profile />
            <History />
        </div>

    </div>

    <Footer />
</template>

<script>
import Footer from '@/pages/master/footer.vue';
import Profile from '@/pages/master/profile.vue';
import History from '@/pages/master/history.vue';
import AdminPost from '@/pages/master/adminPost.vue';
import { useUserStore } from '@/stores/user';

import { useBookingStore } from '@/stores/myFlight';

import apiClient from '@/api/axios';

export default {
    components: {
        Footer,
        Profile,
        History,
        AdminPost
    },
    data() {
        return {
            bookings: [],
            latest_notification: {},
            showDelayNotification: false,
            showSuccessNotification: false,
        };
    },

    async created() {
        const userStore = useUserStore();
        console.log(userStore.user)

        try {
            // get all bookings of an user (information includes flight details, price, meal, luggage, etc.)
            const bookingStore = useBookingStore();

            this.bookings = await bookingStore.fetchBookings(userStore.user.id);

            console.log(this.bookings);
        } catch (error) {
            console.error(error);
            this.$toastr.error('Failed to fetch bookings');
        }

        // get latest notification
        try {
            const response = await apiClient.get(`/notifications/${userStore.user.id}/latest`);

            this.latest_notification = response.data.data.notifications;
            console.log(response.data.data);
            console.log(this.latest_notification);

            if (response.data.data.is_read == true) {
                this.showDelayNotification = false;
                this.showSuccessNotification = false;
            } else if (this.latest_notification.type === 'SCHEDULE_CHANGE') {
                this.showDelayNotification = true;
                this.showSuccessNotification = false;
            } else if (this.latest_notification.type === 'BOOKING_CONFIRMED') {
                this.showDelayNotification = false;
                this.showSuccessNotification = true;
            }
        } catch (error) {
            console.error(error);
            this.$toastr.error('Failed to fetch latest notification');
        }

    },

    methods: {
        // Check if the "Cancel" button should be rendered for a particular booking
        shouldRenderCancelButton(booking) {
            // Get today's date (without time)
            const today = new Date();
            today.setHours(0, 0, 0, 0); // Reset time to midnight for comparison purposes

            // Parse the booking's check-in date (yyyy-mm-dd)
            const checkInDate = new Date(booking.flights[0].checkin);

            // Calculate the difference in days
            const timeDifference = checkInDate - today;
            const daysDifference = timeDifference / (1000 * 3600 * 24); // Convert from milliseconds to days

            // If the difference is greater than 3 days, render the cancel button
            return daysDifference > 3;
        },
        async removeFlight(id) {
            // Lọc bỏ chuyến bay có flightNumber tương ứng
            const response = await apiClient.delete(`/bookings/${id}`);

            this.bookings = this.bookings.filter(booking => booking.id !== id);

            if (response.status == 200) {
                this.$toastr.success('Booking canceled successfully');
            } else {
                this.$toastr.error('Failed to cancel booking');
            }

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
    computed: {
        filteredBookings() {
            if (!this.searchQuery) {
                return this.bookings; // Nếu không có từ khóa tìm kiếm, trả về toàn bộ danh sách
            }
            const query = this.searchQuery.toLowerCase(); // Chuyển từ khóa tìm kiếm về chữ thường để so sánh
            return this.bookings.filter(booking =>
                booking.flights[0].arrival_city.toLowerCase().includes(query)
            );
        }
    }
};
</script>

<style scoped>
.flight-list {
    width: 100%;
    padding: 20px;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px !important;
}

h2 {
    text-align: center;
    color: #333;
    font-size: 1.8rem;
    margin-bottom: 10px !important;
}

.flight-card {
    width: 100%;
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    max-width: 800px;
    background-image: url(@/assets/bookingbg.jpg);
    /* Đặt đường dẫn đến ảnh nền */
    background-size: cover;
    /* Đảm bảo ảnh phủ toàn bộ diện tích của flight-card */
    background-position: center;
    /* Căn giữa ảnh */
    justify-content: space-between;
}

.flight-info-horizontal {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 200px;
    /* Chiều cao cố định để dễ căn chỉnh */
    gap: 40px;
}

/* Cột trái: Thời gian */
.time-column {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    /* Đẩy thời gian lên đầu và xuống cuối */
}

/* Cột giữa: Đường bay */
.route-column {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
}

.icon-departure,
.icon-arrival {
    font-size: 1.2em;
}

.line {
    width: 2px;
    flex: 1;
    background-color: #ccc;
}

.icon-plane {
    width: 26px;
    /* Kích thước nhỏ tùy chọn */
    height: 26px;
    /* Kích thước nhỏ tùy chọn */
}

.icon-location {
    margin-top: 10px;
    width: 24px;
    /* Kích thước nhỏ tùy chọn */
    height: 24px;
    /* Kích thước nhỏ tùy chọn */
}


/* Cột phải: Sân bay */
.airport-column {
    display: flex;
    flex-direction: column;

    /* Đẩy tên sân bay lên đầu và xuống cuối */
    align-items: flex-start;
    /* Căn các phần tử theo chiều ngang */
    height: 100%;
}

/* Các class căn chỉnh cụ thể */
.departure-time,
.departure-airport {
    align-self: flex-start;
}

.arrival-time,
.arrival-airport {
    align-self: flex-start;
    margin: 0;
}

.duration {
    font-size: 1.0em;
    font-weight: bold;
    justify-content: center;
    margin-top: auto;
    /* Tạo khoảng trống phía trên, đẩy xuống giữa */
    margin-bottom: auto;
    /* Tạo khoảng trống phía dưới, giữ ở giữa */
}

/* Kiểu chữ cho thời gian và sân bay */
.time-block {
    font-size: 1.2em;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.airport-block {
    font-size: 1.2em;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.price-info-horizontal {
    display: flex;
    justify-content: space-between;
    width: 100%;
    align-items: center;
}

.price {
    font-size: 1.2em;
    font-weight: bold;
    color: red;
}


.ticket {
    font-size: 1.2em;
    font-weight: bold;
    color: red;
}

.cancel-button {
    padding: 10px 20px;
    background-color: #c7eded;
    color: black;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.cancel-button:hover {
    background-color: #0056b3;
}

.date {
    font-size: 0.8em;
    color: #3331319a;
}

.from,
.to {
    font-size: 0.8em;
    color: #3331319a;
}

.service {
    display: flex;
    flex-direction: column;
    align-items: flex-start !important;
    gap: 10px;
    justify-content: center;
    margin-top: auto;
    /* Tạo khoảng trống phía trên, đẩy xuống giữa */
    margin-bottom: auto;
    /* Tạo khoảng trống phía dưới, giữ ở giữa */
    /* Khoảng cách giữa các mục */
}

.luggage,
.travelers,
.meal {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start !important;
    /* Căn chỉnh theo trục ngang */
    gap: 5px;
    /* Khoảng cách giữa biểu tượng và văn bản */
}

.service-icon {
    width: 18px;
    /* Kích thước nhỏ gọn */
    height: 18px;
    object-fit: contain;
    align-items: flex-start !important;
    /* Đảm bảo không bị méo hình */
}

.service-text {
    font-size: 0.7em;
    color: #3331319a;
    /* Màu xám nhẹ */
    font-weight: bold;
}

.search-bar {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
    width: 100%;
    max-width: 800px;
    margin-bottom: 20px;
}

.icon {
    width: 20px;
    height: 20px;
    margin-right: 8px;
}

.search-input {
    border: none;
    outline: none;
    flex-grow: 1;
    font-size: 14px;
    /* background-color: ; */
}

.myflight-profile {
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin-right: 20px;
}

.profile-weather {
    display: flex;
    flex-direction: column;
    gap: 10px;
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