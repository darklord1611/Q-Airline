<template>
    <div class="ticket-management">
        <!-- Bộ lọc -->
        <div class="filters">
            <div class="filter-row">
                <label for="from">From:</label>
                <select v-model="filters.from">
                    <option value="">All</option>
                    <option value="Hanoi">Hanoi</option>
                    <option value="Ho Chi Minh City">Ho Chi Minh City</option>
                </select>

                <label for="to">To:</label>
                <select v-model="filters.to">
                    <option value="">All</option>
                    <option value="JFK">JFK</option>
                    <option value="LAX">LAX</option>
                </select>
            </div>

            <div class="filter-row">
                <!-- Bộ lọc - Departure Airport -->
                <label for="departureAirport">Departure Airport:</label>
                <select v-model="filters.departureAirport">
                    <option value="">All</option>
                    <option value="JFK">JFK</option>
                    <option value="LAX">LAX</option>
                    <option value="Hanoi">Hanoi</option>
                    <option value="Ho Chi Minh City">Ho Chi Minh City</option>
                </select>

                <!-- Bộ lọc - Arrival Airport -->
                <label for="arrivalAirport">Arrival Airport:</label>
                <select v-model="filters.arrivalAirport">
                    <option value="">All</option>
                    <option value="JFK">JFK</option>
                    <option value="LAX">LAX</option>
                    <option value="Hanoi">Hanoi</option>
                    <option value="Ho Chi Minh City">Ho Chi Minh City</option>
                </select>

                <!-- Bộ lọc - Departure Time -->
                <label for="departureTime">Departure Time:</label>
                <input type="date" v-model="filters.departureTime" />

                <!-- Bộ lọc - Arrival Time -->
                <label for="arrivalTime">Arrival Time:</label>
                <input type="date" v-model="filters.arrivalTime" />

            </div>

            <div class="filter-row">
                <label for="checkinDate">Check-in:</label>
                <input type="date" v-model="filters.checkin" />

                <label for="checkoutDate">Check-out:</label>
                <input type="date" v-model="filters.checkout" />

                <label for="price">Price range:</label>
                <div class="price-range">
                    <input type="range" v-model="filters.minPrice" :max="filters.maxPrice" min="0" step="10"
                        @input="checkPriceOrder" />
                    <input type="range" v-model="filters.maxPrice" :min="filters.minPrice" max="1000" step="10"
                        @input="checkPriceOrder" />
                </div>
                <div class="price-values">
                    <span>Min: {{ filters.minPrice }} USD</span>
                    <span>Max: {{ filters.maxPrice }} USD</span>
                </div>
            </div>

            <div class="filter-row">
                <label for="ticketType">Ticket Type:</label>
                <select v-model="filters.ticketType">
                    <option value="">All</option>
                    <option value="Economy">Economy</option>
                    <option value="Business">Business</option>
                    <option value="First Class">First Class</option>
                </select>

                <label for="travelers">Travelers:</label>
                <input type="number" v-model="filters.travelers" min="1" placeholder="Number of travelers" />

                <label for="meals">Meals:</label>
                <select v-model="filters.meals">
                    <option value="">All</option>
                    <option value="Veg">Veg</option>
                    <option value="Non-Veg">Non-Veg</option>
                </select>

                <label for="luggageWeight">Luggage Weight (kg):</label>
                <input type="number" v-model="filters.luggageWeight" min="0" placeholder="Max weight" />
            </div>
        </div>
        <label class="myheader"> Ticket Management</label>
        <!-- Bảng thống kê -->
        <table class="ticket-table">
            <thead>
                <tr>
                    <th>Ticket Number</th>
                    <th>Travelers</th>
                    <th>From</th>
                    <th>To</th>
                    <th>Check-in</th>
                    <th>Check-out</th>
                    <th>Departure Airport</th>
                    <th>Departure Time</th>
                    <th>Arrival Airport</th>
                    <th>Arrival Time</th>
                    <th>Meals</th>
                    <th>Luggage Weight (kg)</th>
                    <th>Price</th>
                    <th>Ticket Type</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(ticket, index) in paginatedTickets" :key="index">
                    <td>{{ ticket.ticketNumber }}</td>
                    <td>{{ ticket.travelers }}</td>
                    <td>{{ filters.from || ticket.departureAirport }}</td>
                    <td>{{ filters.to || ticket.arrivalAirport }}</td>
                    <td>{{ filters.checkin || 'N/A' }}</td>
                    <td>{{ filters.checkout || 'N/A' }}</td>
                    <td>{{ ticket.departureAirport }}</td>
                    <td>{{ ticket.departureTime }}</td>
                    <td>{{ ticket.arrivalAirport }}</td>
                    <td>{{ ticket.arrivalTime }}</td>
                    <td>{{ ticket.meals }}</td>
                    <td>{{ ticket.luggageWeight }}</td>
                    <td>{{ ticket.price }}</td>
                    <td>{{ ticket.ticketType }}</td>
                </tr>
            </tbody>
        </table>

        <!-- Phân trang -->
        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            filters: {
                from: "",
                to: "",
                checkin: "",
                checkout: "",
                departureAirport: "",
                arrivalAirport: "",
                departureTime: "",
                arrivalTime: "",
                minPrice: 0,
                maxPrice: 1000,
                ticketType: "",
                travelers: "",
                meals: "",
                luggageWeight: ""
            },
            tickets: [
                {
                    ticketNumber: "T123",
                    travelers: 2,
                    departureAirport: "JFK",
                    arrivalAirport: "LAX",
                    checkin: "2024-12-10",
                    checkout: "2024-12-12",
                    departureAirport: "JFK",
                    departureTime: "2024-12-10",
                    arrivalAirport: "LAX",
                    arrivalTime: "2024-12-10",
                    meals: "Veg",
                    luggageWeight: 20,
                    price: "$350",
                    ticketType: "Economy"
                },
                {
                    ticketNumber: "T456",
                    travelers: 1,
                    departureAirport: "Hanoi",
                    arrivalAirport: "Ho Chi Minh City",
                    checkin: "2024-12-15",
                    checkout: "2024-12-16",
                    departureAirport: "JFK",
                    departureTime: "2024-12-10",
                    arrivalAirport: "LAX",
                    arrivalTime: "2024-12-10",
                    meals: "Non-Veg",
                    luggageWeight: 25,
                    price: "$120",
                    ticketType: "Business"
                },
                {
                    ticketNumber: "T789",
                    travelers: 3,
                    departureAirport: "LAX",
                    arrivalAirport: "JFK",
                    checkin: "2024-12-18",
                    checkout: "2024-12-19",
                    departureAirport: "JFK",
                    departureTime: "2024-12-10",
                    arrivalAirport: "LAX",
                    arrivalTime: "2024-12-10",
                    meals: "Veg",
                    luggageWeight: 30,
                    price: "$600",
                    ticketType: "First Class"
                }
            ],
            currentPage: 1,
            pageSize: 4
        };
    },
    computed: {
        filteredTickets() {
            return this.tickets.filter(ticket => {
                const matchFrom = !this.filters.from || ticket.departureAirport === this.filters.from;
                const matchTo = !this.filters.to || ticket.arrivalAirport === this.filters.to;
                const matchCheckin = !this.filters.checkin || true;
                const matchCheckout = !this.filters.checkout || true;
                const matchDepartureAirport = !this.filters.departureAirport || ticket.departureAirport === this.filters.departureAirport;
                const matchArrivalAirport = !this.filters.arrivalAirport || ticket.arrivalAirport === this.filters.arrivalAirport;
                const matchDepartureTime = !this.filters.departureTime || ticket.departureTime === this.filters.departureTime;
                const matchArrivalTime = !this.filters.arrivalTime || ticket.arrivalTime === this.filters.arrivalTime;
                const matchPrice =
                    parseFloat(ticket.price.replace('$', '')) >= this.filters.minPrice &&
                    parseFloat(ticket.price.replace('$', '')) <= this.filters.maxPrice;
                const matchTicketType = !this.filters.ticketType || ticket.ticketType === this.filters.ticketType;
                const matchTravelers = !this.filters.travelers || ticket.travelers == this.filters.travelers;
                const matchMeals = !this.filters.meals || ticket.meals === this.filters.meals;
                const matchLuggageWeight =
                    !this.filters.luggageWeight || ticket.luggageWeight <= this.filters.luggageWeight;

                return matchFrom && matchTo && matchCheckin && matchCheckout && matchDepartureAirport && matchArrivalAirport && matchDepartureTime && matchArrivalTime && matchPrice && matchTicketType && matchTravelers && matchMeals && matchLuggageWeight;
            });
        },
        totalPages() {
            return Math.ceil(this.filteredTickets.length / this.pageSize);
        },
        paginatedTickets() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredTickets.slice(start, end);
        }
    },
    methods: {
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        checkPriceOrder() {
            if (this.filters.minPrice > this.filters.maxPrice) {
                this.filters.maxPrice = this.filters.minPrice;
            }
        }
    }
};
</script>

<style scoped>
/* Phần chính */
.ticket-management {
    width: 90%;
    margin: auto;
    text-align: center;
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    /* Nền tổng thể */
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

/* Bảng vé */
.ticket-table {
    width: 100% !important;
    max-width: 800px !important;
    border-collapse: collapse;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff;
}

.ticket-table thead {
    background-color: #003D5B;
    color: #ffffff;
    font-weight: bold;
}

.ticket-table thead th {
    padding: 12px;
    text-align: center;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.ticket-table tbody tr {
    transition: all 0.3s ease;
}

.ticket-table tbody tr:nth-child(even) {
    background-color: #e6f2f8;
}

.ticket-table tbody tr:nth-child(odd) {
    background-color: #ffffff;
}

.ticket-table tbody tr:hover {
    background-color: #cce6f0;
    transform: scale(1.01);
    cursor: pointer;
}

.ticket-table tbody td {
    padding: 10px;
    text-align: center;
    font-size: 13px;
    color: #333333;
    border-bottom: 1px solid #cccccc;
    word-wrap: break-word;
}

/* Bộ lọc */
.filters {
    margin: 20px 0;
}

.filter-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 10px;
    align-items: center;
}

input[type="date"],
select {
    padding: 8px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    font-size: 13px;
    width: 150px;
    text-align: center;
}

input[type="date"]:focus,
select:focus {
    outline: none;
    border-color: #003D5B;
    box-shadow: 0 0 5px rgba(0, 61, 91, 0.5);
}

/* Thanh kéo giá */
.price-range {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.price-range input[type="range"] {
    -webkit-appearance: none;
    width: 200px;
    height: 6px;
    background: #d9d9d9;
    border-radius: 4px;
    outline: none;
}

.price-range input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 14px;
    height: 14px;
    background: #003D5B;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.price-range input[type="range"]::-moz-range-thumb {
    width: 14px;
    height: 14px;
    background: #003D5B;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.price-values {
    font-size: 13px;
    color: #555555;
    display: flex;
    justify-content: space-between;
    width: 200px;
}

/* Phân trang */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    font-size: 14px;
    gap: 10px;
}

.pagination button {
    background-color: #003D5B;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.pagination button:hover {
    background-color: #005377;
}

.pagination button:disabled {
    background-color: #999999;
    cursor: not-allowed;
}

.pagination span {
    font-weight: bold;
    color: #003D5B;
}

@media (max-width: 768px) {
    .ticket-table {
        width: 100%;
        /* Bảng co giãn đầy đủ theo màn hình */
        max-width: 100%;
        /* Giới hạn không vượt quá chiều rộng màn hình */
        table-layout: fixed;
        /* Bố trí các ô đồng đều */
    }

    .ticket-table td,
    .ticket-table th {
        word-wrap: break-word;
        /* Cắt nội dung nếu quá dài */
        overflow: hidden;
        text-overflow: ellipsis;
        /* Thay bằng dấu "..." nếu nội dung quá dài */
    }
}

.myheader {
    text-align: center;
    color: #333;
    font-size: 1.8rem;
    margin-bottom: 10px !important;
    font-family: 'Merriweather', serif;
}
</style>
