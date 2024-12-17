<template>
    <div>
        <div style="width: 100%; overflow-x: auto;">
            <canvas id="flightChart" style="min-width: 1200px;"></canvas>
        </div>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
    name: "FlightChart",
    data() {
        return {
            flights: [
                { flightNumber: "AA101", economyTickets: 150, businessTickets: 50, economyRevenue: 30000, businessRevenue: 40000 },
                { flightNumber: "AA102", economyTickets: 200, businessTickets: 60, economyRevenue: 40000, businessRevenue: 50000 },
                { flightNumber: "AA103", economyTickets: 180, businessTickets: 80, economyRevenue: 36000, businessRevenue: 64000 },
                { flightNumber: "AA104", economyTickets: 120, businessTickets: 40, economyRevenue: 24000, businessRevenue: 32000 },
                { flightNumber: "AA105", economyTickets: 100, businessTickets: 30, economyRevenue: 20000, businessRevenue: 24000 },
                { flightNumber: "AA106", economyTickets: 170, businessTickets: 70, economyRevenue: 34000, businessRevenue: 56000 },
                { flightNumber: "AA107", economyTickets: 130, businessTickets: 50, economyRevenue: 26000, businessRevenue: 40000 },
                { flightNumber: "AA108", economyTickets: 190, businessTickets: 90, economyRevenue: 38000, businessRevenue: 72000 },
                { flightNumber: "AA109", economyTickets: 140, businessTickets: 60, economyRevenue: 28000, businessRevenue: 48000 },
                { flightNumber: "AA110", economyTickets: 160, businessTickets: 70, economyRevenue: 32000, businessRevenue: 56000 },
                { flightNumber: "AA111", economyTickets: 110, businessTickets: 30, economyRevenue: 22000, businessRevenue: 24000 },
                { flightNumber: "AA112", economyTickets: 200, businessTickets: 100, economyRevenue: 40000, businessRevenue: 80000 },
                { flightNumber: "AA113", economyTickets: 150, businessTickets: 50, economyRevenue: 30000, businessRevenue: 40000 },
                { flightNumber: "AA114", economyTickets: 180, businessTickets: 80, economyRevenue: 36000, businessRevenue: 64000 },
                { flightNumber: "AA115", economyTickets: 120, businessTickets: 40, economyRevenue: 24000, businessRevenue: 32000 },
                { flightNumber: "AA116", economyTickets: 100, businessTickets: 30, economyRevenue: 20000, businessRevenue: 24000 },
                { flightNumber: "AA117", economyTickets: 170, businessTickets: 70, economyRevenue: 34000, businessRevenue: 56000 },
                { flightNumber: "AA118", economyTickets: 130, businessTickets: 50, economyRevenue: 26000, businessRevenue: 40000 },
                { flightNumber: "AA119", economyTickets: 190, businessTickets: 90, economyRevenue: 38000, businessRevenue: 72000 },
                { flightNumber: "AA120", economyTickets: 140, businessTickets: 60, economyRevenue: 28000, businessRevenue: 48000 }
            ]
        };
    },
    methods: {
        renderChart() {
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
    mounted() {
        this.renderChart();
    },
};
</script>

<style scoped>
#flightChart {
    height: 700px;
}
</style>