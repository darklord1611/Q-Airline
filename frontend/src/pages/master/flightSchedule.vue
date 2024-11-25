<template>
  <div class="flight-search">
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

        <label for="checkinDate">Check-in:</label>
        <input type="date" v-model="filters.checkin" />
      </div>

      <div class="filter-row">
        <label for="checkoutDate">Check-out:</label>
        <input type="date" v-model="filters.checkout" />

        <label for="price">Price range:</label>
        <div class="price-range">
          <!-- Thanh trượt với min và max -->
          <input type="range" 
                 v-model="filters.minPrice" 
                 :max="filters.maxPrice" 
                 min="0" 
                 step="10"
                 @input="checkPriceOrder" 
                 class="min-range"/>
          <input type="range" 
                 v-model="filters.maxPrice" 
                 :min="filters.minPrice" 
                 max="1000" 
                 step="10"
                 @input="checkPriceOrder" 
                 class="max-range"/>
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
      </div>
    </div>

    <!-- Bảng kết quả -->
    <table class="flight-table">
      <thead>
        <tr>
          <th>Flight Number</th>
          <th>From</th>
          <th>To</th>
          <th>Check-in</th>
          <th>Check-out</th>
          <th>Departure Airport</th>
          <th>Departure Time</th>
          <th>Arrival Airport</th>
          <th>Arrival Time</th>
          <th>Duration</th>
          <th>Price</th>
          <th>Ticket Type</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(flight, index) in paginatedFlights" :key="index">
          <td>{{ flight.flightNumber }}</td>
          <td>{{ filters.from || flight.departureAirport }}</td>
          <td>{{ filters.to || flight.arrivalAirport }}</td>
          <td>{{ filters.checkin || 'N/A' }}</td>
          <td>{{ filters.checkout || 'N/A' }}</td>
          <td>{{ flight.departureAirport }}</td>
          <td>{{ flight.departureTime }}</td>
          <td>{{ flight.arrivalAirport }}</td>
          <td>{{ flight.arrivalTime }}</td>
          <td>{{ flight.duration }}</td>
          <td>{{ flight.price }}</td>
          <td>{{ flight.ticketType }}</td>
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
        minPrice: 0,
        maxPrice: 1000,
        ticketType: "" // Thêm bộ lọc loại vé
      },
      flights: [
        {
          departureAirport: "JFK",
          departureTime: "08:00 AM",
          arrivalAirport: "LAX",
          arrivalTime: "11:30 AM",
          flightNumber: "AA123",
          duration: "5h 30m",
          price: "$299",
          ticketType: "Economy"
        },
        {
          departureAirport: "Hanoi",
          departureTime: "06:00 AM",
          arrivalAirport: "Ho Chi Minh City",
          arrivalTime: "08:30 AM",
          flightNumber: "VN456",
          duration: "2h 30m",
          price: "$120",
          ticketType: "Business"
        },
        {
          departureAirport: "LAX",
          departureTime: "09:00 AM",
          arrivalAirport: "JFK",
          arrivalTime: "12:30 PM",
          flightNumber: "AA789",
          duration: "5h 30m",
          price: "$450",
          ticketType: "First Class"
        }
      ],
      currentPage: 1,
      pageSize: 10
    };
  },
  computed: {
    filteredFlights() {
      return this.flights.filter(flight => {
        const matchFrom = !this.filters.from || flight.departureAirport === this.filters.from;
        const matchTo = !this.filters.to || flight.arrivalAirport === this.filters.to;
        const matchCheckin = !this.filters.checkin || true; // Logic kiểm tra ngày check-in
        const matchCheckout = !this.filters.checkout || true; // Logic kiểm tra ngày check-out
        const matchPrice = 
          parseFloat(flight.price.replace('$', '')) >= this.filters.minPrice &&
          parseFloat(flight.price.replace('$', '')) <= this.filters.maxPrice;
        const matchTicketType = !this.filters.ticketType || flight.ticketType === this.filters.ticketType;

        return matchFrom && matchTo && matchCheckin && matchCheckout && matchPrice && matchTicketType;
      });
    },
    totalPages() {
      return Math.ceil(this.filteredFlights.length / this.pageSize);
    },
    paginatedFlights() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredFlights.slice(start, end);
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
.flight-search {
  width: 80%;
  margin: auto;
  text-align: center;
}

.filters {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 10px;
}

.filter-row label {
  font-weight: bold;
}

.filters input[type="range"] {
  width: 100%;
}

.filters .price-range {
  display: flex;
  justify-content: space-between;
}

.filters input[type="range"] + span {
  margin-left: 10px;
}

.filters .price-values {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  gap: 10px;
}

.flight-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.flight-table th,
.flight-table td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
  width: calc(100% / 12);
}

.flight-table th {
  background-color: #f4f4f4;
  color: #333;
}

.flight-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.flight-table tr:hover {
  background-color: #f1f1f1;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
