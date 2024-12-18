<template>
    <div>
        <div style="width: 100%; overflow-x: auto;">
            <canvas id="flightChart" style="min-width: 1200px;"></canvas>
        </div>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

import apiClient from "@/api/axios";

export default {
    name: "FlightChart",
    data() {
        return {
            flights: []
        };
    },
    async created() {
        try {
            // Fetch flight data from API
            const response = await apiClient.get("/flights/analytics/all");

            this.newFlights = response.data.data;

            this.flights = this.newFlights.map(flight => {
                // Initialize the ticket and revenue values
                flight.economyTickets = 0;
                flight.businessTickets = 0;
                flight.economyRevenue = 0;
                flight.businessRevenue = 0;

                for (let i = 0; i < flight.services.length; i++) {
                    if (flight.services[i].name === "ECONOMY") {
                        flight.economyTickets = flight.services[i].count || 0;
                        flight.economyRevenue = flight.services[i].revenue || 0;
                    } else if (flight.services[i].name === "BUSINESS") {
                        flight.businessTickets = flight.services[i].count || 0;
                        flight.businessRevenue = flight.services[i].revenue || 0;
                    }
                }

                return {
                    flightId: flight.flight_id,
                    flightNumber: flight.flight_number,
                    economyTickets: flight.economyTickets,
                    businessTickets: flight.businessTickets,
                    economyRevenue: flight.economyRevenue,
                    businessRevenue: flight.businessRevenue
                };
            });

            console.log("Already mapped:", this.flights);

            // Render the chart after the data is ready
            this.$nextTick(() => {
                this.renderChart();
            });
        } catch (error) {
            console.error("Error fetching flight data:", error);
        }
    },
    methods: {
        renderChart() {
            if (!this.flights.length) {
                console.warn("No flight data available to render chart.");
                return;
            }
            const labels = this.flights.map(flight => flight.flightNumber);
            const economyTickets = this.flights.map(flight => flight.economyTickets);
            const businessTickets = this.flights.map(flight => flight.businessTickets);
            const economyRevenues = this.flights.map(flight => flight.economyRevenue);
            const businessRevenues = this.flights.map(flight => flight.businessRevenue);

            const visibleFlights = 10; // Số chuyến bay hiển thị mỗi lần
            const canvasWidth = visibleFlights * 160; // Mỗi chuyến bay chiếm 120px

            const ctx = document.getElementById("flightChart").getContext("2d");
            document.getElementById("flightChart").style.width = `${canvasWidth}px`;

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Economy Tickets",
                            data: economyTickets,
                            backgroundColor: "#243B4A",
                        },
                        {
                            label: "Business Tickets",
                            data: businessTickets,
                            backgroundColor: "#D1495B",
                        },
                    ],
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const index = context.dataIndex;
                                    const type = context.dataset.label;
                                    const revenue =
                                        type === "Economy Tickets"
                                            ? economyRevenues[index]
                                            : businessRevenues[index];
                                    return `${type}: ${context.raw} (Revenue: $${revenue})`;
                                },
                            },
                        },
                        legend: {
                            position: "top",
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Flight Numbers",
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Number of Tickets",
                            },
                        },
                    },
                },
            });
        },
    },
};
</script>

<style scoped>
#flightChart {
    height: 700px;
}
</style>