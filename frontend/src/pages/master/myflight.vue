<template>
    <div class="flight-list">
        <div class="flight-card" v-for="booking in bookings" :key="booking.id">
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
                <button class="cancel-button" @click="removeFlight(flight.flightNumber)">Cancel</button>
            </div>
        </div>
    </div>
    <Footer />
</template>

<script>
import Footer from '@/pages/master/footer.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';

export default {
    components: {
        Footer
    },
    data() {
        return {
            flights: [
                {
                    departureAirport: "JFK",
                    departureTime: "08:00 AM",
                    arrivalAirport: "LAX",
                    arrivalTime: "11:30 AM",
                    flightNumber: "AA123",
                    duration: "5h30m",
                    price: "$299",
                    ticketType: "Economy",
                    from: "New York",
                    to: "Los Angeles",
                    checkin: "2024-11-25",
                    checkout: "2024-11-25",
                    luggage: "8 kg",
                    meal: "3 meals",
                    travelers: "3 travelers"
                },
                {
                    departureAirport: "SFO",
                    departureTime: "09:15 AM",
                    arrivalAirport: "ORD",
                    arrivalTime: "03:45 PM",
                    flightNumber: "UA456",
                    duration: "4h30m",
                    price: "$259",
                    ticketType: "Business",
                    from: "San Francisco",
                    to: "Chicago",
                    checkin: "2024-11-26",
                    checkout: "2024-11-26",
                    luggage: "8 kg",
                    meal: "3 meals",
                    travelers: "3 travelers"
                },
                {
                    departureAirport: "LHR",
                    departureTime: "02:30 PM",
                    arrivalAirport: "DXB",
                    arrivalTime: "12:15 AM",
                    flightNumber: "EK789",
                    duration: "7h45m",
                    price: "$599",
                    ticketType: "First Class",
                    from: "London",
                    to: "Dubai",
                    checkin: "2024-11-27",
                    checkout: "2024-11-28",
                    luggage: "8 kg",
                    meal: "3 meals",
                    travelers: "3 travelers"
                }
            ],
            bookings: []
        };
    },

    async created() {
        const userStore = useUserStore();
        console.log(userStore.user)

        // get all bookings of an user (information includes flight details, price, meal, luggage, etc.)
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/bookings?user_id=${userStore.user.id}`);


        // Định dạng ngày tháng ngay khi component được khởi tạo

        this.bookings = response.data.data;

        console.log(this.bookings);

        this.bookings = this.bookings.map((booking) => ({
            ...booking,
            totalMeal: this.calcTotalMeal(booking.flights[0].services),
            totalLuggage: this.calcTotalLuggage(booking.flights[0].services),
            formattedCheckIn: this.formatDate(booking.flights[0].checkin),
            formattedCheckOut: this.formatDate(booking.flights[0].checkout),
        }));

        console.log(this.bookings);

        this.flights = this.flights.map((flight) => ({
            ...flight,
            formattedCheckIn: this.formatDate(flight.checkin),
            formattedCheckOut: this.formatDate(flight.checkout),
        }));
    },

    methods: {
        formatDate(inputDate) {
            // Chuyển đổi định dạng ngày tháng
            const date = new Date(inputDate);
            const options = { weekday: "short", day: "numeric", month: "short" };
            return date.toLocaleDateString("en-US", options);
        },
        removeFlight(flightNumber) {
            // Lọc bỏ chuyến bay có flightNumber tương ứng
            this.flights = this.flights.filter(flight => flight.flightNumber !== flightNumber);
        },
        calcTotalMeal(services) {
            console.log(services);
            return services.reduce((total, service) => {
                if (service.services.type === 'MEAL') {
                    total += service.quantity;
                }
                return total;
            }, 0);
        },
        calcTotalLuggage(services) {
            console.log(services);
            return services.reduce((total, service) => {
                if (service.services.type === 'LUGGAGE') {
                    total += service.quantity;
                }
                return total;
            }, 0);
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
</style>