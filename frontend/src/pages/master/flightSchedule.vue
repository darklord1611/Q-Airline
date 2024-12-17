<template>
  <TicketManage />
  <div class="flight-search">
    <div class="header-row">
      <label class="myheader">Flight Schedule</label>
      <div class="over-table">
        <button @click="toggleAircraft" class="add-aircraft-btn">
          <img src="@/assets/plus.png" class="add-aircraft-icon" /> Add Aircraft
        </button>
        <button @click="toggleFilters" class="filter-btn">
          <img src="@/assets/filter.png" alt="Filter Icon" class="filter-icon" /> Filter
        </button>
        <button class="sort-btn">
          <img src="@/assets/arrow.png" class="sort-icon" /> Sort
        </button>
      </div>
    </div>
    <table class="flight-table">
      <thead>
        <tr>
          <th>Flight Number</th>
          <th>From</th>
          <th>To</th>
          <th>Departure Time</th>
          <th>Arrival Time</th>
          <th>Price</th>
          <th>Ticket Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(flight, index) in paginatedFlights" :key="index">
          <td>{{ flight.flightNumber }}</td>
          <td>{{ flight.from }}</td>
          <td>{{ flight.to }}</td>
          <td>{{ flight.departureTime }}</td>
          <td>{{ flight.arrivalTime }}</td>
          <td>{{ flight.price }}</td>
          <td>{{ flight.ticketType }}</td>
          <td v-if="isAdmin"> <img src="@/assets/edit.png" alt="Details" @click="openModal(flight)"
              style="cursor: pointer; width: 24px; height: 30px;" /></td>
          <td v-if="!isAdmin"> <img src="@/assets/search-file.png" alt="Details" @click="openModal(flight)"
              style="cursor: pointer; width: 24px; height: 30px;" /></td>
        </tr>
      </tbody>
    </table>
    <!-- Popover-Aircraft -->
    <div v-if="showAircraft" class="aircraft-popover" :style="aircraftPopoverStyle">
      <h3 class="text-lg font-semibold mb-4">Add Aircraft Details</h3>

      <!-- Model -->
      <div class="mb-3">
        <label for="model" class="block text-sm font-medium text-gray-700 mb-1">Model</label>
        <input type="text" id="model" v-model="aircraft.model"
          class="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
          placeholder="Enter aircraft model" />
      </div>

      <!-- Manufacturer -->
      <div class="mb-3">
        <label for="manufacturer" class="block text-sm font-medium text-gray-700 mb-0.2">Manufacturer</label>
        <input type="text" id="manufacturer" v-model="aircraft.manufacturer"
          class="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
          placeholder="Enter manufacturer name" />
      </div>

      <!-- Business Seats -->
      <div class="mb-3">
        <label for="business" class="block text-sm font-medium text-gray-700 mb-0.2">Business Seats</label>
        <input type="number" id="business" v-model="aircraft.business"
          class="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
          placeholder="Enter number of business seats" />
      </div>

      <!-- Economy Seats -->
      <div class="mb-3">
        <label for="economy" class="block text-sm font-medium text-gray-700 mb-0.2">Economy Seats</label>
        <input type="number" id="economy" v-model="aircraft.economy"
          class="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
          placeholder="Enter number of economy seats" />
      </div>

      <!-- Submit Button -->
      <div class="flex justify-end">
        <button type="button" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          @click="handleSubmit">
          Submit
        </button>
      </div>
    </div>

    <!-- Popover-filter -->
    <div v-if="showFilters" class="filters-popover" :style="popoverStyle">
      <!-- Hàng 1: From và To -->
      <div class="filter-row">
        <div class="filter-title half-width">From:</div>
        <div class="filter-title half-width">To:</div>
      </div>

      <!-- Hàng 2: Bộ lọc From và To -->
      <div class="filter-row">
        <select v-model="filters.from" class="half-width">
          <option value="">All</option>
          <option value="Hanoi">Hanoi</option>
          <option value="Ho Chi Minh City">Ho Chi Minh City</option>
        </select>
        <select v-model="filters.to" class="half-width">
          <option value="">All</option>
          <option value="JFK">JFK</option>
          <option value="LAX">LAX</option>
        </select>
      </div>

      <!-- Hàng 3: Departure Time và Arrival Time -->
      <div class="filter-row">
        <div class="filter-title half-width">Departure Time:</div>
        <div class="filter-title half-width">Arrival Time:</div>
      </div>

      <!-- Hàng 4: Bộ lọc Departure Time và Arrival Time -->
      <div class="filter-row">
        <input type="date" v-model="filters.departureTime" class="half-width" />
        <input type="date" v-model="filters.arrivalTime" class="half-width" />
      </div>

      <!-- Hàng 5: Ticket Type -->
      <div class="filter-row">
        <div class="filter-title full-width">Ticket Type:</div>
      </div>

      <!-- Hàng 6: Bộ lọc Ticket Type -->
      <div class="filter-row">
        <select v-model="filters.ticketType" class="full-width">
          <option value="">All</option>
          <option value="Economy">Economy</option>
          <option value="Business">Business</option>
          <option value="First Class">First Class</option>
        </select>
      </div>

      <!-- Hàng 9: Price Range -->
      <div class="filter-row">
        <div class="filter-title full-width">Price Range:</div>
      </div>

      <!-- Hàng 10: Bộ lọc Price Range -->
      <div class="filter-row">
        <div class="price-range full-width">
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

      <!-- Hàng cuối: Nút Clear và Apply -->
      <div class="filter-actions">
        <button @click="clearFilters" class="clear-btn">Clear</button>
        <button @click="applyFilters" class="apply-btn">Apply</button>
      </div>
    </div>
  </div>
  <!-- Bảng kết quả -->


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
      aircraft: {
        model: "",
        manufacturer: "",
        business: null,
        economy: null,
      },
      selectedFlight: null,
      originalFlight: null,
      isAdmin: false,
      popoverStyle: {},
      showFilters: false,
      showAircraft: false,
      filters: {
        from: "",
        to: "",
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
          price: "$299",
          ticketType: "Economy",
          from: "HN",
          to: "HCM"
        },
        {
          departureAirport: "Hanoi",
          departureTime: "06:00 AM",
          arrivalAirport: "Ho Chi Minh City",
          arrivalTime: "08:30 AM",
          flightNumber: "VN456",
          price: "$120",
          ticketType: "Business",
          from: "HNR",
          to: "BGLG"
        },
        {
          departureAirport: "LAX",
          departureTime: "09:00 AM",
          arrivalAirport: "JFK",
          arrivalTime: "12:30 PM",
          flightNumber: "AA789",
          price: "$450",
          ticketType: "First Class",
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
        const matchDepartureTime = !this.filters.departureTime || flight.departureTime === this.filters.departureTime;
        const matchArrivalTime = !this.filters.arrivalTime || flight.arrivalTime === this.filters.arrivalTime;

        const matchPrice =
          parseFloat(flight.price.replace('$', '')) >= this.filters.minPrice &&
          parseFloat(flight.price.replace('$', '')) <= this.filters.maxPrice;

        const matchTicketType = !this.filters.ticketType || flight.ticketType === this.filters.ticketType;

        return matchFrom && matchTo && matchDepartureTime && matchArrivalTime && matchPrice && matchTicketType;
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
    },

    toggleFilters(event) {
      const button = event.target.closest(".filter-btn");
      if (this.showFilters) {
        this.showFilters = false; // Close the popover
      } else {
        // Calculate position
        const rect = button.getBoundingClientRect();
        const popoverWidth = 415;
        this.popoverStyle = {
          top: `${rect.bottom + window.scrollY}px`,
          left: `${rect.right - popoverWidth}px`,
          position: "absolute",
          zIndex: 1000,
        };
        this.showFilters = true;
      }
    },

    toggleAircraft(event) {
      const button = event.target.closest(".add-aircraft-btn");
      if (this.showAircraft) {
        this.showAircraft = false; // Đóng popover
      } else {
        // Tính toán vị trí hiển thị
        const rect = button.getBoundingClientRect();
        const popoverWidth = 415; // Chiều rộng popover giả định
        this.aircraftPopoverStyle = {
          top: `${rect.bottom + window.scrollY}px`,
          left: `${rect.right - popoverWidth}px`,
          position: "absolute",
          zIndex: 1000,
        };
        this.showAircraft = true;
      }
    },


    clearFilters() {
      this.filters = {
        from: '',
        to: '',
        ticketType: '',
        departureTime: '',
        arrivalTime: '',
        minPrice: 0,
        maxPrice: 1000,
      };
    },
    applyFilters() {
      console.log("Filters applied:", this.filters);
      this.showFilters = false; // Close after applying
    },

    handleSubmit() {
      console.log("Aircraft Details:", this.aircraft);
      // Reset the form after submission
      this.aircraft = {
        model: "",
        manufacturer: "",
        business: null,
        economy: null,
      };
      this.showAircraft = false; // Close the popover
    },
  }
};
</script>

<style scoped>
.flight-search {
  width: 100%;
  /* Đặt giới hạn độ rộng tối đa */
  margin: auto;
  text-align: center;
  font-family: 'Arial', sans-serif;
  /* Font đơn giản và dễ đọc */
  border-radius: 12px;
  /* Bo tròn viền mượt mà */
  border: 1px solid #d4d4d4;
  /* Màu viền nhạt */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* Thêm bóng đổ mềm mại */
  background-color: #ffffff;
  /* Màu nền trắng */
  overflow: hidden;
  /* Đảm bảo nội dung bên trong không bị tràn */
}

/* Bảng chính */
.flight-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /* Thêm bóng đổ */
  /* Bo góc mềm mại */
  overflow: hidden;
  background-color: #f9f9f9;
  /* Màu nền chung */
  table-layout: fixed;
}

/* Header */
.flight-table thead {
  background: linear-gradient(135deg, #003D5B, #00577A);
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
  align-items: flex-start;
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

.filter-container {
  position: relative;
}

.header-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
}

.add-aircraft-btn,
.sort-btn,
.filter-btn {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}

.add-aircraft-icon,
.sort-icon,
.filter-icon {
  width: 16px;
  height: 16px;
  margin-right: 0.5rem;
}

/* Popover styles */
.aircraft-popover,
.filters-popover {
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  width: 400px;
  /* Độ rộng cố định của popover */
  max-width: 100%;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 0.4rem;
  justify-content: center;
}

.filter-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.half-width {
  width: 50%;
  padding-right: 0.5rem;
  box-sizing: border-box;
}

.full-width {
  width: 100%;
}

.price-range {
  display: flex;
  gap: 0.5rem;
}

.price-values {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.clear-btn,
.apply-btn {
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.clear-btn {
  background-color: #f8d7da;
  color: #721c24;
}

.apply-btn {
  background-color: #d4edda;
  color: #155724;
}

.over-table {
  display: flex;
  flex-direction: row;
  gap: 5px;
}
</style>
