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

        <label for="ticketType">Ticket Type:</label>
        <select v-model="filters.ticketType">
          <option value="">All</option>
          <option value="Economy">Economy</option>
          <option value="Business">Business</option>
          <option value="First Class">First Class</option>
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
    </div>
    <label class="myheader"> Flight Schedule</label>
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
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(flight, index) in paginatedFlights" :key="index">
          <td>{{ flight.flightNumber }}</td>
          <td>{{ flight.departureAirport }}</td>
          <td>{{ flight.arrivalAirport }}</td>
          <td>{{ flight.checkin }}</td>
          <td>{{ flight.checkout }}</td>
          <td>{{ flight.departureAirport }}</td>
          <td>{{ flight.departureTime }}</td>
          <td>{{ flight.arrivalAirport }}</td>
          <td>{{ flight.arrivalTime }}</td>
          <td>{{ flight.duration }}</td>
          <td>{{ flight.price }}</td>
          <td>{{ flight.ticketType }}</td>
          <td v-if="isAdmin"> <img src="@/assets/edit.png" alt="Details" @click="openModal(flight)"
              style="cursor: pointer; width: 24px; height: 30px;" /></td>
          <td v-if="!isAdmin"> <img src="@/assets/search-file.png" alt="Details" @click="openModal(flight)"
              style="cursor: pointer; width: 24px; height: 30px;" /></td>
        </tr>
      </tbody>
    </table>

    <div v-if="selectedFlight && !isAdmin" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="time-duration">
          <div class="time-view">
            <label class="big-text">{{ selectedFlight.departureTime }}</label>
            <label class="small-text">{{ selectedFlight.departureAirport }}</label>
            <img src="@/assets/watchPlane.png" class="watch-icon">
            <label class="big-text">{{ selectedFlight.arrivalTime }}</label>
            <label class="small-text">{{ selectedFlight.arrivalAirport }}</label>
          </div>
          <label class="small-text">{{ selectedFlight.duration }}</label>
        </div>
        <div class="airport-view">
          <div class="airport-view-column">
            <div class="block">
              <label class="big-text">{{ selectedFlight.departureAirport }}</label>
              <label class="small-text">{{ selectedFlight.departureTime }}</label>
            </div>
            <div class="block">
              <label class="big-text">{{ selectedFlight.arrivalAirport }}</label>
              <label class="small-text">{{ selectedFlight.arrivalTime }}</label>
            </div>
          </div>
          <div class="route-column">
            <div class="dot">●</div>
            <div class="line"></div>
            <div class="dot">●</div>
          </div>
          <div class="airport-view-column">
            <label class="big-text">{{ selectedFlight.from }}</label>
            <div class="block">
              <label class="small-text">{{ selectedFlight.flightNumber }}</label>
              <label class="small-text">{{ selectedFlight.ticketType }}</label>
              <label class="small-text">{{ selectedFlight.price }}</label>
            </div>
            <label class="big-text">{{ selectedFlight.to }}</label>
          </div>
        </div>
        <div class="but-row">
          <div class="closeBut">
            <button @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedFlight && isAdmin" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>Flight Edit</h3>
        <div class="modal-fields">
          <!-- Các trường nhập liệu trong modal -->
          <div class="edit-line">
            <label for="flightNumber">Flight Number:</label>
            <input type="text" v-model="selectedFlight.flightNumber" />
          </div>

          <div class="edit-line">
            <label for="departureAirport">Departure Airport:</label>
            <input type="text" v-model="selectedFlight.departureAirport" />
          </div>

          <div class="edit-line">
            <label for="arrivalAirport">Arrival Airport:</label>
            <input type="text" v-model="selectedFlight.arrivalAirport" />
          </div>

          <div class="edit-line">
            <label for="departureTime">Departure Time:</label>
            <input type="time" v-model="selectedFlight.departureTime" />
          </div>

          <div class="edit-line">
            <label for="arrivalTime">Arrival Time:</label>
            <input type="time" v-model="selectedFlight.arrivalTime" />
          </div>

          <div class="edit-line">
            <label for="checkinDate">Check-in:</label>
            <input type="date" v-model="selectedFlight.checkin" />
            <label for="checkoutDate">Check-out:</label>
            <input type="date" v-model="selectedFlight.checkout" />
          </div>


          <div class="edit-line">
            <label for="price">Price:</label>
            <input type="text" v-model="selectedFlight.price" />
          </div>

          <div class="edit-line">
            <label for="ticketType">Ticket Type:</label>
            <select v-model="selectedFlight.ticketType">
              <option value="Economy">Economy</option>
              <option value="Business">Business</option>
              <option value="First Class">First Class</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="applyChanges">Apply</button>
          <button @click="closeModal">Close</button>
        </div>
      </div>
    </div>




    <!-- Phân trang -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
  <TicketManage />
  <Footer />
</template>

<script>
import Footer from '@/pages/master/footer.vue';
import TicketManage from '@/pages/master/ticketManage.vue';
export default {
  components: {
    Footer,
    TicketManage
  },
  data() {
    return {
      selectedFlight: null,
      originalFlight: null,
      isAdmin: false,
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
          ticketType: "Economy",
          checkin: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          checkout: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          from: "HN",
          to: "HCM"
        },
        {
          departureAirport: "Hanoi",
          departureTime: "06:00 AM",
          arrivalAirport: "Ho Chi Minh City",
          arrivalTime: "08:30 AM",
          flightNumber: "VN456",
          duration: "2h 30m",
          price: "$120",
          ticketType: "Business",
          checkin: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          checkout: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          from: "HNR",
          to: "BGLG"
        },
        {
          departureAirport: "LAX",
          departureTime: "09:00 AM",
          arrivalAirport: "JFK",
          arrivalTime: "12:30 PM",
          flightNumber: "AA789",
          duration: "5h 30m",
          price: "$450",
          ticketType: "First Class",
          checkin: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          checkout: "2024-12-05",  // Thay đổi thành định dạng YYYY-MM-DD
          from: "HNN",
          to: "UET"
        }
      ],


      currentPage: 1,
      pageSize: 4
    };
  },
  computed: {
    filteredFlights() {
      return this.flights.filter(flight => {
        const matchFrom = !this.filters.from || flight.from === this.filters.from;
        const matchTo = !this.filters.to || flight.to === this.filters.to;

        // Kiểm tra ngày check-in và check-out
        const matchCheckin = !this.filters.checkin || flight.checkin === this.filters.checkin;
        const matchCheckout = !this.filters.checkout || flight.checkout === this.filters.checkout;

        const matchDepartureAirport = !this.filters.departureAirport || flight.departureAirport === this.filters.departureAirport;
        const matchArrivalAirport = !this.filters.arrivalAirport || flight.arrivalAirport === this.filters.arrivalAirport;
        const matchDepartureTime = !this.filters.departureTime || flight.departureTime === this.filters.departureTime;
        const matchArrivalTime = !this.filters.arrivalTime || flight.arrivalTime === this.filters.arrivalTime;

        const matchPrice =
          parseFloat(flight.price.replace('$', '')) >= this.filters.minPrice &&
          parseFloat(flight.price.replace('$', '')) <= this.filters.maxPrice;

        const matchTicketType = !this.filters.ticketType || flight.ticketType === this.filters.ticketType;

        return matchFrom && matchTo && matchCheckin && matchCheckout && matchDepartureAirport && matchArrivalAirport && matchDepartureTime && matchArrivalTime && matchPrice && matchTicketType;
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
    openModal(flight) {
      this.selectedFlight = { ...flight };// Lưu thông tin của dòng được chọn
      this.originalFlight = { ...flight }; // Lưu bản sao gốc để khôi phục khi đóng modal
    },
    closeModal() {
      this.selectedFlight = null; // Đóng modal và không thay đổi gì
      this.originalFlight = null;  // Đặt lại bản sao gốc
    },
    applyChanges() {
      const hasChanges = Object.keys(this.selectedFlight).some(key => {
        return this.selectedFlight[key] !== this.originalFlight[key];
      });

      if (hasChanges) {
        const index = this.flights.findIndex(flight => flight.flightNumber === this.selectedFlight.flightNumber);
        if (index !== -1) {
          this.flights.splice(index, 1, { ...this.selectedFlight }); // Cập nhật chuyến bay
        }
      }
      this.closeModal(); // Đóng modal sau khi thay đổi
    },

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
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /* Thêm bóng đổ */
  border-radius: 8px;
  /* Bo góc mềm mại */
  overflow: hidden;
  background-color: #f9f9f9;
  /* Màu nền chung */
  table-layout: fixed;
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
  font-size: 11px;
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

.myheader {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 10px !important;
  font-family: 'Merriweather', serif;
}

.modal-overlay {
  position: fixed;
  top: 0;
  right: 0;
  /* Modal sẽ xuất hiện ở bên phải màn hình */
  width: 100%;
  /* Chiều rộng chiếm 35% màn hình */
  height: 100%;
  /* Chiều cao chiếm 100% chiều cao màn hình */
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  /* Căn trái để modal sát bên phải */
  align-items: flex-start;
  /* Căn top để modal bắt đầu từ trên cùng */
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 20px;
  width: 45%;
  height: 100%;
  /* Đảm bảo modal không vượt quá chiều cao của màn hình */
  overflow-y: auto;
  /* Cho phép cuộn nếu nội dung quá dài */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 5px;
  position: relative;
  /* Để tạo không gian cho các nút phía dưới */
}

.modal-content h3 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #003D5B;
  margin-bottom: 5px;
}

.modal-fields {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-fields label {
  font-size: 14px;
  font-weight: bold;
  color: #555;
}

.modal-fields input,
.modal-fields select {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  width: 100%;
  max-width: 350px;
  box-sizing: border-box;
}

.modal-fields input[type="datetime-local"] {
  width: auto;
  padding: 8px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  position: absolute;
  /* Đặt các nút vào cuối cùng của modal */
  bottom: 0px;
  width: calc(100% - 40px);
  /* Đảm bảo các nút không bị tràn ra ngoài */
}

.edit-line {
  display: flex;
  flex-direction: row;
  gap: 5px;
  justify-content: flex-end;
}

.closeBut,
.modal-actions button {
  margin-top: 30px;
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #003D5B;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 48%;
  /* Chia đều cho hai nút */
}

.modal-actions button:hover {
  background-color: #1F7D8C;
}

.modal-actions button:focus {
  outline: none;
}

.modal-actions button:disabled {
  background-color: #999;
  cursor: not-allowed;
}


.flight-table td:last-child {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;

}

.flight-table th:last-child,
.flight-table td:last-child {
  width: 75px !important;
  /* Điều chỉnh giá trị này tùy thuộc vào nhu cầu */
}

.flight-table td,
.flight-table th {
  height: 61px;
  /* Đặt chiều cao cho tất cả các ô, bạn có thể điều chỉnh giá trị này */
  vertical-align: middle;
  /* Căn giữa theo chiều dọc cho tất cả các ô */
}

.flight-table tr {
  height: 61px;
  /* Đảm bảo chiều cao của hàng giống nhau */
}

.time-view {
  display: flex;
  flex-direction: row;
  gap: 5px;
  justify-content: center;
}

.watch-icon {
  height: 40px;
  Width: 40px;
  margin-left: 10px;
  margin-right: 10px;
}

.big-text {
  font-size: 2.1em;
}

.small-text {
  font-size: 1.3em;
}

.time-duration {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #000;
  align-items: center;
  padding-top: 30px;
  padding-bottom: 10px;
}

.airport-view {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: 60%;
  /* Chiều cao cố định để dễ căn chỉnh */
  gap: 40px;
}

.airport-view-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 40px;
}

.block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.route-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.dot {
  font-size: 1.2em;
}

.line {
  width: 2px;
  height: 600px;
  background-color: #ccc;
}

.but-row {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
</style>
