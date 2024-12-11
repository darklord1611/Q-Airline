<template>
  <div class="flight-search">

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
      </div>
    </div>
  </div>
  <Footer />
</template>

<script>
import Footer from '@/pages/master/footer.vue';
export default {
  components: {
    Footer
  },
  data() {
    return {
      isAdmin: true,
      filters: {
        from: "",
        to: "",
        checkin: "",
        checkout: "",
        minPrice: 0,
        maxPrice: 1000,
        ticketType: ""
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
      pageSize: 4
    };
  },
  computed: {
    filteredFlights() {
      return this.flights.filter(flight => {
        const matchFrom = !this.filters.from || flight.departureAirport === this.filters.from;
        const matchTo = !this.filters.to || flight.arrivalAirport === this.filters.to;
        const matchCheckin = !this.filters.checkin || true;
        const matchCheckout = !this.filters.checkout || true;
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
  width: 90%;
  /* Tăng độ rộng để phù hợp với màn hình lớn hơn */
  margin: auto;
  text-align: center;
  font-family: 'Arial', sans-serif;
  /* Thay đổi font mặc định */
}

/* Bảng chính */
.flight-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /* Thêm bóng đổ */
  border-radius: 8px;
  /* Bo góc mềm mại */
  overflow: hidden;
  background-color: #f9f9f9;
  /* Màu nền chung */
}

/* Header */
.flight-table thead {
  background-color: #003D5B;
  /* Màu header */
  color: #ffffff;
  /* Màu chữ trắng */
  font-weight: bold;
}

.flight-table thead th {
  padding: 12px;
  text-align: center;
  font-size: 14px;
  letter-spacing: 1px;
  /* Tạo khoảng cách giữa các chữ */
  text-transform: uppercase;
  /* Chuyển chữ thành in hoa */
}

/* Body */
.flight-table tbody tr {
  transition: all 0.3s ease;
  /* Thêm hiệu ứng hover mượt */
}

.flight-table tbody tr:nth-child(even) {
  background-color: #e6f2f8;
  /* Màu nền dòng chẵn */
}

.flight-table tbody tr:nth-child(odd) {
  background-color: #ffffff;
  /* Màu nền dòng lẻ */
}

.flight-table tbody tr:hover {
  background-color: #cce6f0;
  /* Màu nền khi hover */
  transform: scale(1.01);
  /* Hiệu ứng phóng to nhẹ */
  cursor: pointer;
}

.flight-table tbody td {
  padding: 10px;
  text-align: center;
  font-size: 13px;
  color: #333333;
  /* Màu chữ */
  border-bottom: 1px solid #cccccc;
  /* Đường gạch dưới giữa các dòng */
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
  /* Màu nền chính */
  color: #ffffff;
  /* Màu chữ */
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  /* Bo góc nhẹ */
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination button:hover {
  background-color: #005377;
  /* Màu khi hover */
}

.pagination button:disabled {
  background-color: #999999;
  /* Màu khi bị vô hiệu */
  cursor: not-allowed;
}

.pagination span {
  font-weight: bold;
  color: #003D5B;
  /* Màu chữ nổi bật */
}

/* Bộ lọc */
.filters {
  margin-top: 20px;
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
  /* Đặt chiều rộng cố định để đồng đều */
  text-align: center;
  /* Canh giữa văn bản bên trong */
}

input[type="date"]:focus,
select:focus {
  outline: none;
  border-color: #003D5B;
  /* Màu viền khi focus */
  box-shadow: 0 0 5px rgba(0, 61, 91, 0.5);
  /* Hiệu ứng focus */
}

/* Thanh kéo giá (Price Range) */
.price-range {
  display: flex;
  flex-direction: column;
  /* Chuyển thành cột để dễ quản lý */
  align-items: center;
  gap: 8px;
  /* Tạo khoảng cách giữa hai thanh kéo */
}

.price-range input[type="range"] {
  -webkit-appearance: none;
  /* Bỏ kiểu mặc định */
  width: 200px;
  /* Chiều rộng của thanh kéo */
  height: 6px;
  background: #d9d9d9;
  /* Màu nền của thanh kéo */
  border-radius: 4px;
  outline: none;
}

.price-range input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: #003D5B;
  /* Màu của đầu kéo */
  border-radius: 50%;
  /* Hình tròn */
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.price-range input[type="range"]::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: #003D5B;
  /* Màu của đầu kéo */
  border-radius: 50%;
  /* Hình tròn */
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.price-values {
  font-size: 13px;
  color: #555555;
  display: flex;
  justify-content: space-between;
  width: 200px;
  /* Đồng bộ với chiều rộng của thanh kéo */
}
</style>
