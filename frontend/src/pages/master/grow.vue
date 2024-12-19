<template>
    <div class="dashboard-container">
        <!-- Header Section -->
        <div class="header-section">
            <!-- Revenue Summary -->
            <div class="revenue-summary">
                <div class="header-col">
                    <h1 class="totalRevenue">{{ totalRevenue.title }}</h1>
                    <p class="month">{{ totalRevenue.date }}</p>
                </div>
                <div>
                    <div class="revenue-details">
                        <span class="revenue-value">{{ totalRevenue.value }}</span>
                        <img :src="icons.arrowUp" alt="Growth Icon" class="icon-image" />
                        <label> {{ totalRevenue.growth }} </label>
                    </div>
                    <p class="performance-message">
                        {{ totalRevenue.performanceMessage }}
                        <img :src="icons.arm" alt="Performance Icon" class="icon-image" />
                    </p>
                </div>
            </div>
            <!-- Revenue Chart -->
            <div class="revenue-chart">
                <canvas ref="revenueChart" class="chart"></canvas>
            </div>
        </div>

        <!-- Statistics Section -->
        <div class="statistics-section">
            <div class="statistic-item" v-for="(stat, index) in statistics" :key="index">
                <div class="row-static">
                    <img :src="stat.icon" alt="Stat Icon" class="stat-icon-image" />
                    <h4 class="statistic-name">{{ stat.name }}</h4>
                </div>
                <p class="data-static">{{ stat.value }}</p>
            </div>
        </div>
    </div>
</template>

<script>
// Import necessary icons
import upIcon from "@/assets/up.png";
import bicepsIcon from "@/assets/biceps.png";
import passengerIcon from "@/assets/passenger-data.png";
import mealIcon from "@/assets/meal-data.png";
import flightIcon from "@/assets/flight-data.png";
import airlinesIcon from "@/assets/airlines-data.png";

import apiClient from "@/api/axios";

// Import Chart.js library
import { Chart, registerables } from "chart.js";

// Register Chart.js components
Chart.register(...registerables);

export default {
    name: "PerformanceDashboard",
    data() {
        return {
            totalRevenue: {
                title: "Total Revenue",
                date: "",
                value: "",
                growth: "",
                performanceMessage: "",
            },
            icons: {
                arrowUp: upIcon,
                arm: bicepsIcon,
            },
            statistics: [
                { name: "Total Passengers", value: "", icon: passengerIcon },
                { name: "Service Revenue", value: "", icon: mealIcon },
                { name: "Flights Happened", value: "", icon: flightIcon },
                { name: "Airlines Available", value: "", icon: airlinesIcon },
            ],
            revenueData: [], // To store revenue data for the chart
        };
    },
    async created() {
        try {
            // Fetch total revenue data from the API
            const response = await apiClient.get(`/flights/yearly_analytics/2024`);
            const data = response.data.data;

            // Process the data
            this.processApiData(data);
        } catch (error) {
            console.error("Error fetching analytics data:", error);
        }
    },
    methods: {
        processApiData(data) {
            // Fill in the revenue chart data and calculate growth
            this.revenueData = data.map(item => item.total_revenue);

            // Calculate total revenue for December and growth from November
            const decRevenue = data.find(item => item.month === 12)?.total_revenue || 0;
            const novRevenue = data.find(item => item.month === 11)?.total_revenue || 0;
            const growth = novRevenue > 0 ? ((decRevenue - novRevenue) / novRevenue) * 100 : 0;

            this.totalRevenue = {
                title: "Total Revenue",
                date: "December 2024",
                value: `$${decRevenue.toLocaleString(undefined, { minimumFractionDigits: 2 })}`,
                growth: `${growth.toFixed(2)}%`,
                performanceMessage: growth >= 0 ? "You have a great performance" : "Performance needs improvement",
            };

            // Fill in the statistics
            const totalPassengers = data.reduce((acc, cur) => acc + (cur.total_tickets || 0), 0);
            const totalFlights = data.reduce((acc, cur) => acc + (cur.total_flights || 0), 0);

            this.statistics = [
                { name: "Total Passengers", value: totalPassengers.toLocaleString(), icon: passengerIcon },
                { name: "Service Revenue", value: `$${this.revenueData.reduce((a, b) => a + b, 0).toLocaleString()}`, icon: mealIcon },
                { name: "Flights Happened", value: totalFlights.toLocaleString(), icon: flightIcon },
                { name: "Airlines Available", value: "4", icon: airlinesIcon }, // Placeholder as API doesn't provide airline count
            ];

            // Generate the revenue growth chart
            this.generateChart();
        },
        generateChart() {
            const ctx = this.$refs.revenueChart.getContext("2d");
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: [
                        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                    ],
                    datasets: [
                        {
                            label: "Revenue Growth",
                            data: this.revenueData,
                            borderColor: "#003D5B",
                            backgroundColor: "rgba(0, 61, 91, 0.1)",
                            fill: true,
                            borderWidth: 2,
                            pointRadius: 3,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { display: true },
                        y: { display: true },
                    },
                    plugins: {
                        legend: { display: false },
                    },
                },
            });
        },
    },
};
</script>


<style scoped>
.dashboard-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 20px;
    margin: 20px;
}

.header-section {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 20px;
}

.revenue-summary {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    width: 40%;
}

.revenue-details {
    display: flex;
    align-items: center;
    flex-direction: row;
    gap: 10px;
    font-weight: bold;
}

.performance-message {
    display: flex;
    align-items: center;
    font-size: 1em;
    gap: 5px;
    border: 1px solid #ccc;
    border-radius: 10px;
    margin-bottom: 10px;
    width: 63%;
    font-weight: bold;
}

.icon-image,
.stat-icon-image {
    width: 24px;
    height: 24px;
    margin-right: 5px;
}

.revenue-chart {
    width: 60%;
    height: 250px;
}

.statistics-section {
    display: flex;
    flex-direction: row;
    width: 100%;
}

.statistic-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
    flex: 1;
    height: 120px;
    border-right: 2px solid #ccc;
    padding-left: 10px;
    /* Đường viền phải màu xám mờ */
    /* Tạo khoảng cách giữa nội dung và border */
}

.statistic-item:last-child {
    border-right: none;
}

.stat-icon-image {
    width: 90px;
    height: 70px;
}

.totalRevenue {
    font-weight: bold;
    font-size: 25px;
}

.header-col {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.month {
    font-size: 16px;
}

.revenue-value {
    font-size: 4.0rem;
}

.row-static {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
}

.statistic-name {
    font-weight: bold;
    text-align: left;
}

.data-static {
    font-size: 40px;
    font-weight: bold;
}
</style>
