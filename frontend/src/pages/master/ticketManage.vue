<template>
    <div class="ticket-management">
        <label class="myheader"> Ticket Management</label>

        <!-- Biểu đồ cột -->
        <div>
            <canvas id="ticketChart" style="width: 100%; height: 400px;"></canvas>
        </div>

        <!-- Bảng liệt kê các tàu bay -->
        <table class="ticket-table">
            <thead>
                <tr>
                    <th>Aircraft Code</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(aircraft, index) in aircrafts" :key="index">
                    <td>{{ aircraft.code }}</td>
                    <td><button @click="showDetails(index)">Detail</button></td>
                </tr>
            </tbody>
        </table>

        <!-- Bảng chi tiết vé -->
        <div v-if="selectedAircraftIndex !== null" class="ticket-details">
            <h3>Tickets for Aircraft {{ aircrafts[selectedAircraftIndex].code }}</h3>
            <table class="ticket-table">
                <thead>
                    <tr>
                        <th>Ticket Number</th>
                        <th>Travelers</th>
                        <th>From</th>
                        <th>To</th>
                        <th>Check-in</th>
                        <th>Check-out</th>
                        <th>Departure Time</th>
                        <th>Arrival Time</th>
                        <th>Meals</th>
                        <th>Luggage Weight (kg)</th>
                        <th>Price</th>
                        <th>Ticket Type</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(ticket, index) in aircrafts[selectedAircraftIndex].tickets" :key="index">
                        <td>{{ ticket.ticketNumber }}</td>
                        <td>{{ ticket.travelers }}</td>
                        <td>{{ ticket.departureAirport }}</td>
                        <td>{{ ticket.arrivalAirport }}</td>
                        <td>{{ ticket.checkin }}</td>
                        <td>{{ ticket.checkout }}</td>
                        <td>{{ ticket.departureTime }}</td>
                        <td>{{ ticket.arrivalTime }}</td>
                        <td>{{ ticket.meals }}</td>
                        <td>{{ ticket.luggageWeight }}</td>
                        <td>{{ ticket.price }}</td>
                        <td>{{ ticket.ticketType }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { Chart } from 'chart.js/auto';

export default {
    data() {
        return {
            aircrafts: [
                {
                    code: "A123",
                    tickets: [
                        {
                            ticketNumber: "T001",
                            travelers: 2,
                            departureAirport: "JFK",
                            arrivalAirport: "LAX",
                            checkin: "2024-12-10",
                            checkout: "2024-12-12",
                            departureTime: "10:00 AM",
                            arrivalTime: "1:00 PM",
                            meals: "Veg",
                            luggageWeight: 20,
                            price: "$350",
                            ticketType: "Economy"
                        },
                        {
                            ticketNumber: "T002",
                            travelers: 1,
                            departureAirport: "JFK",
                            arrivalAirport: "LAX",
                            checkin: "2024-12-10",
                            checkout: "2024-12-12",
                            departureTime: "10:00 AM",
                            arrivalTime: "1:00 PM",
                            meals: "Non-Veg",
                            luggageWeight: 25,
                            price: "$450",
                            ticketType: "Business"
                        }
                    ]
                },
                {
                    code: "B456",
                    tickets: [
                        {
                            ticketNumber: "T003",
                            travelers: 3,
                            departureAirport: "Hanoi",
                            arrivalAirport: "Ho Chi Minh City",
                            checkin: "2024-12-15",
                            checkout: "2024-12-16",
                            departureTime: "9:00 AM",
                            arrivalTime: "11:00 AM",
                            meals: "Veg",
                            luggageWeight: 30,
                            price: "$120",
                            ticketType: "Economy"
                        }
                    ]
                }
            ],
            selectedAircraftIndex: null
        };
    },
    methods: {
        showDetails(index) {
            this.selectedAircraftIndex = index;
        },
        renderChart() {
            const ctx = document.getElementById('ticketChart').getContext('2d');

            const labels = this.aircrafts.map(aircraft => aircraft.code);
            const economyTickets = this.aircrafts.map(aircraft =>
                aircraft.tickets.filter(ticket => ticket.ticketType === 'Economy').length
            );
            const businessTickets = this.aircrafts.map(aircraft =>
                aircraft.tickets.filter(ticket => ticket.ticketType === 'Business').length
            );

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels,
                    datasets: [
                        {
                            label: 'Economy',
                            data: economyTickets,
                            backgroundColor: '#243B4A',
                            barThickness: 20 // Độ rộng cột nhỏ lại
                        },
                        {
                            label: 'Business',
                            data: businessTickets,
                            backgroundColor: '#D1495B',
                            barThickness: 20 // Độ rộng cột nhỏ lại
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top' // Vị trí của chú thích
                        }
                    },
                    scales: {
                        x: {
                            stacked: false // Không xếp chồng
                        },
                        y: {
                            beginAtZero: true,
                            max: 5 // Giới hạn trục dọc tối đa là 5
                        }
                    }
                }
            });
        }
    },
    mounted() {
        this.renderChart();
    }
};
</script>
<style scoped>
/* Phần chính */
.ticket-management {
    width: 100%;
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

.ticket-details {
    margin-top: 20px;
}

.ticket-details h3 {
    color: #003D5B;
    margin-bottom: 10px;
}

.ticket-details table {
    margin-top: 10px;
}
</style>
