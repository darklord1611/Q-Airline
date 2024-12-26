<template>
  <div class="bookingflexcontainer">
    <div class="slogan">
      <h1>Wings To Your Dreams</h1>
    </div>

    <div class="bookingfaceflex">
      <div class="videoD">
        <video :src="video" autoplay muted loop class="video"></video>
      </div>
      <img :src="image" class="planeimage" />
    </div>

    <div class="overlay"></div>
    <div class="flight-search-container">
      <div class="input-group">
        <!-- From Dropdown -->
        <div class="input-field">
          <div class="input-icon">
            <img :src="fromTo" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">From</label>
            <select v-model="airports.departureAirport" @change="updateToOptions" class="typeIn">
              <option v-for="airport in airports.fromOptions" :key="airport.id" :value="airport">
                {{ airport.city }} ({{ airport.iata_code }})
              </option>
            </select>
          </div>
        </div>

        <!-- To Dropdown -->
        <div class="input-field">
          <div class="input-icon">
            <img :src="fromTo" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">To</label>
            <select v-model="airports.arrivalAirport" class="typeIn">
              <option v-for="airport in airports.toOptions" :key="airport.id" :value="airport">
                {{ airport.city }} ({{ airport.iata_code }})
              </option>
            </select>
          </div>
        </div>

        <!-- Checkin Dropdown -->
        <div class="input-field">
          <div class="input-icon">
            <img :src="calendar" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">
              Departure Date
            </label>
            <input type="date" ref="checkInDate" @change="handleDateChange('checkInDate')" class="typeIn" />
          </div>
        </div>

        <!-- Checkout Dropdown -->
        <!-- <div class="input-field">
          <div class="input-icon">
            <img :src="calendar" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">
              Check Out
            </label>
            <input type="date" ref="checkOutDate" @change="handleDateChange('checkOutDate')" class="typeIn" />
          </div>
        </div> -->
        <!-- search flights button-->
        <button class="search-btn" @click="searchFlights">Search Flight</button>
      </div>
    </div>

    <div class="image-slider-container">
      <button @click="prevSlide" class="prev-btn">&#10094;</button>
      <div class="image-slider">
        <div class="slider-item" v-for="(item, index) in items" :key="index" v-show="currentIndex === index">
          <img :src="item.image" :alt="'Image ' + (index + 1)">
          <div class="text-overlay">{{ item.text }}</div>
        </div>
        <div :class="{
          'discount-buttons': user !== null,
          'discount-buttons-admin': isAdmin === true,
        }">
          <div v-for="(item, index) in items" :key="index" class="button-container">
            <button class="discount-button" :class="{ active: activeButtonIndex === index }"
              @click="handleDiscountButtonClick(index)">
              {{ item.title }}
            </button>
            <button v-if="isAdmin" class="circle-button" @click="handleRemoveDiscountClick(index)">
              -
            </button>
          </div>
        </div>
      </div>
      <button @click="nextSlide" class="next-btn">&#10095;</button>
    </div>

    <div v-if="loading">
      <Loading />
    </div>

    <div class="flight-list" v-if="isSearched && !loading">
      <h1 class="title">Available Flights</h1>
      <div class="flight-card" v-for="flight in filteredFlights" :key="flight.id">
        <div class="ticket-icon">
          <img src="@/assets/flight.png" alt="take off icon" class="takeOff" />
        </div>
        <div class="headerInfo">
          <div class="airlineText">
            Qairline
          </div>
          <div class="flightnumber">
            {{ flight.flight_number }} - {{ selectedClass }}
          </div>
        </div>
        <div class="time">
          <div class="departureTime"> {{ flight.departure_time }}</div>
          <div class="dateConvert"> {{ flight.formattedDepartureTime }}</div>
        </div>
        <div class="ticket-tour">
          <div class="icons">
            <img src="@/assets/take-off (1).png" alt="takeoff icon" class="icon takeoff" />
            <div class="duration">
              Duration: <span class="time2">{{ flight.duration }}</span>
            </div>
            <img src="@/assets/landing.png" alt="landing icon" class="icon landing" />
          </div>
          <div class="progress-bar">
            <div class="line"></div>
            <div class="circle left"></div>
            <div class="circle right"></div>
          </div>
          <div class="labels">
            <span class="label">{{ airports.departureAirport.iata_code }}</span>
            <span class="label B">Direct</span>
            <span class="label">{{ airports.arrivalAirport.iata_code }}</span>
          </div>
        </div>
        <div class="time">
          <div class="arivalTime"> {{ flight.arrival_time }}</div>
          <div class="dateConvert"> {{ flight.formattedArrivalTime }}</div>
        </div>
        <!-- Thông tin giá và nút chọn -->
        <div class="price-info">
          <button class="select-button-economy" v-if="!isChoosed"
            @click="selectFlight(flight, flight.class_pricing[0].class_name)">
            <span class="icon-ticket">
              <img src="@/assets/economy-ticket-whitee.png" alt="Economy Icon" class="icon-ticket-image" />
            </span>
            Economy
            <span class="price-economy">${{ flight.class_pricing[0].base_price }} USD</span>
          </button>
          <button class="select-button-bussiness" v-if="!isChoosed"
            @click="selectFlight(flight, flight.class_pricing[1].class_name)">
            <span class="icon-ticket">
              <img src="@/assets/bussiness-ticket-black.png" alt="Economy Icon" class="icon-ticket-image" />
            </span>
            Bussiness
            <span class="price-bussiness">${{ flight.class_pricing[1].base_price }} USD</span>
          </button>
          <button class="select-button-economy" v-if="isEconomyChoosed" @click="undoFlight()"><label class="Undo">Undo
            </label>
          </button>
          <button class="select-button-bussiness" v-if="isBussinessChoosed" @click="undoFlight()"><label
              class="Undo">Undo</label>
          </button>
        </div>
      </div>
    </div>

    <!-- chọn ghế ngồi -->
    <div class="service-container" v-if="isService">
      <h1 class="title">Selecting Seats</h1>
      <div class="seat-choosing">
        <img src="@/assets/seatImage2.jpg" class="seatImage" />

        <div class="seat-choose-info">
          <div class="passenger-numbers-row">
            <label for="passenger-count" style="font-weight: bold;">Passengers:</label>
            <input style="background-color: #f9f9f9;font-weight: bold;" id="passenger-count" type="number" min="1"
              v-model.number="passengerCount" @input="updatePassengers" />
          </div>
          <div class="passenger-list">
            <div v-for="(passenger, index) in this.booking.passengers" :key="index" class="passenger-card">
              <img src="@/assets/traveler-icon.png" class="fromToImage" />
              <span style="font-weight: bold;">Passenger {{ index + 1 }}</span>
              <span>Place: <input type="text" v-model="passenger.place" placeholder="_ _"
                  style="background-color: #f9f9f9;font-weight: bold;" /></span>
            </div>
          </div>
          <div class="seat-status-info">
            <div class="status-item">
              <div class="status-box" style="background-color: green;"></div>
              <span>Successful</span>
            </div>
            <div class="status-item">
              <div class="status-box" style="background-color: #D1495B;"></div>
              <span>Business</span>
            </div>
            <div class="status-item">
              <div class="status-box" style="background-color: #243B4A;"></div>
              <span>Economy</span>
            </div>
            <div class="status-item">
              <div class="status-box" style="background-color: gray;"></div>
              <span>Booked</span>
            </div>
          </div>
        </div>

        <div class="seat-layout">
          <!-- Hiển thị hàng A, B, C -->
          <div v-for="row in topRows" :key="row" class="seat-row">
            <span class="row-label">{{ row }}</span>
            <div v-for="column in seatColumns" :key="column" class="seat-container">
              <button class="seat" :class="{ booked: seats[`${column}${row}`].isBooked }"
                :style="getSeatStyle(column, row, seats[`${column}${row}`].isBooked)"
                @click="toggleSeatSelection(`${column}${row}`)"></button>
            </div>
          </div>

          <!-- Hiển thị số thứ tự từ 1 đến 10 -->
          <div class="seat-row numbers">
            <span class="row-label"></span>
            <div v-for="column in seatColumns" :key="'number-' + column" class="number">
              {{ column }}
            </div>
          </div>

          <!-- Hiển thị hàng D, E, F -->
          <div v-for="row in bottomRows" :key="row" class="seat-row">
            <span class="row-label">{{ row }}</span>
            <div v-for="column in seatColumns" :key="column" class="seat-container">
              <button class="seat" :class="{ booked: seats[`${column}${row}`].isBooked }"
                :style="getSeatStyle(column, row, seats[`${column}${row}`].isBooked)"
                @click="toggleSeatSelection(`${column}${row}`)"></button>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- lựa chọn meal -->
    <div class="service-container" v-if="isService">
      <h1 class="title">Qmeal Service</h1>
      <div class="meal-list">
        <div class="meal-card" v-for="meal in externalServices.meals" :key="meal.name">
          <img class="meal-img" :src="meal.img_src" alt="meal image" />
          <div class="meal-description">
            <h3 class="large-label">{{ meal.name }}</h3>
            <p>{{ meal.description }}</p>
          </div>
          <div class="meal-price"></div>
          <div class="meal-quantity">
            <input type="number" v-model="meal.quantity" min="0" class="input-quantity" />
          </div>
        </div>
      </div>
    </div>
    <div class="luggage-finish" v-if="isService">
      <div class="baggage-slider">
        <h1 class="title">Qluggage Service</h1>
        <!-- Thanh kéo -->
        <div class="slider-container">
          <div class="track">
            <!-- Phần màu sắc hiển thị khi kéo -->
            <div class="filled" :style="{ width: `${(selectedWeight / maxWeight) * 100}%` }"></div>
          </div>
          <div class="thumb" :style="{ left: `${(selectedWeight / maxWeight) * 100}%` }" @mousedown="startDragging">
            <img src="@/assets/suitcase.png" alt="Luggage Icon" class="luggage-icon" draggable="false" />
          </div>
        </div>
        <!-- Hiển thị cân nặng -->
        <div class="weight-display">
          <span>{{ selectedWeight }} kg</span>
          <span> - </span>
          <span>{{ calculatePrice(selectedWeight) }} $USD</span>
        </div>
      </div>

      <div class="total-price-info">
        <span class="price">Total: ${{ totalPrice }} USD</span>
        <button class="select-button" @click="createBooking()">Finish!</button>
      </div>
    </div>

    <News />
    <div v-once>
      <Introduction />
      <TopTraveler />
    </div>
    <TrendingDes />
    <Footer />
  </div>
</template>

<script>
import video from "@/assets/58475-488682084_small.mp4";
import image from "@/assets/vecteezy_plane-png-with-ai-generated_26773766.png";
import fromTo from "@/assets/pin.png";
import calendar from "@/assets/calendar.png";
import Footer from '@/pages/master/footer.vue';
import { faker } from '@faker-js/faker';
import News from '@/pages/master/news.vue';
import apiClient from "@/api/axios";
import { useUserStore } from '@/stores/user';
import { useAirportStore } from "@/stores/airports";
import TrendingDes from '@/pages/master/trendingDestination.vue';
import Introduction from "@/pages/master/introduction.vue";
import TopTraveler from "@/pages/master/topTraveler.vue";
import { useBookingStore } from "@/stores/myFlight";
import Loading from "@/pages/master/loading.vue";
import { ElMessageBox, ElMessage } from "element-plus";


export default {
  components: {
    Footer,
    News,
    TrendingDes,
    Introduction,
    TopTraveler,
    Loading
  },
  name: "booking",
  data() {
    return {
      loading: false,
      isAdmin: false,
      user: null,
      totalPrice: 0,
      selectedWeight: 0, // Giá trị ban đầu của số cân nặng
      maxWeight: 20, // Số cân tối đa
      dragging: false, // Trạng thái kéo
      activeButtonIndex: null,
      topRows: ['A', 'B', 'C'],
      bottomRows: ['D', 'E', 'F'],
      seatColumns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      selectedSeats: [],
      formattedDates: {
        checkIn: '',
        checkOut: ''
      },
      video,
      image,
      fromTo,
      calendar,
      classOptions: ['Economy', 'Business Class'],
      selectedClass: 'Economy',
      isSearched: false,
      isChoosed: false,
      isEconomyChoosed: false,
      isBussinessChoosed: false,
      isService: false,
      selectedFlight: {
        flightInfo: null,
        seats: []
      },
      currentIndex: 0,
      items: [],
      airports: {
        defaultOptions: [],
        fromOptions: [],
        toOptions: [],
        departureAirport: null,
        arrivalAirport: null
      },
      flights: [],
      externalServices: {
        meals: [],
        luggage: [],
        luggageService: null,
      },
      externalServiceCount: [],
      booking: {
        passengers: [],
      },
      passengerCount: 1,
      bookingStore: null
    };
  },
  watch: {
    // Watch for changes in passengerCount
    passengerCount: "updatePassengers",
  },
  async created() {
    const userStore = useUserStore();
    this.user = userStore.user;
    this.isAdmin = userStore.isAdmin;

    const bookingStore = useBookingStore();
    this.bookingStore = bookingStore;

    const airportStore = useAirportStore()

    try {
      // Fetch airports from the store (which handles fetching and caching)
      this.airports.defaultOptions = await airportStore.fetchAirports()
      this.airports.fromOptions = [...this.airports.defaultOptions];
      this.airports.toOptions = [...this.airports.defaultOptions];

    } catch (error) {
      console.error("Error fetching initial airports:", error);
      this.$toastr.error("Error fetching airports. Please try again.");
    }

    try {
      // fetch all discounts
      const response = await apiClient.get(`/discounts`);
      console.log(response.data.data);
      this.items = response.data.data.map((discount) => ({
        id: discount.id,
        image: discount.image_url,
        text: discount.description,
        startDate: new Date(discount.start_time),
        endDate: new Date(discount.end_time),
        title: discount.name,
        discountFactor: discount.discount_factor
      }));
    } catch (error) {
      console.log("Error fetching discounts:", error);
      this.$toastr.error("Error fetching discounts. Please try again.");
    }


    try {
      // Fetching external services like meals or luggage
      const response = await apiClient.get(`/services/search?service_type=MEAL`);
      this.externalServices.meals = response.data.data;

      const luggage_response = await apiClient.get(`/services/search?service_type=LUGGAGE`);
      this.externalServices.luggage = luggage_response.data.data;
      this.externalServices.luggageService = this.externalServices.luggage.find(service => service.id === 11);

    } catch (error) {
      console.log(error)
      this.$toastr.error("Error fetching external services. Please try again.");
    }

  },

  computed: {
    filteredFlights() {
      if (!this.selectedFlight.flightInfo) return this.flights;
      return this.flights.filter(
        (flight) => flight.flight_number === this.selectedFlight.flightInfo.flight_number
      );
    },

    totalPrice() {
      if (!this.selectedFlight) return 0;
      let oneTicketPrice = null;
      if (this.isEconomyChoosed) {
        oneTicketPrice = this.selectedFlight.flightInfo.class_pricing[0].base_price;
      } else {
        oneTicketPrice = this.selectedFlight.flightInfo.class_pricing[1].base_price;
      }

      // compare seletected flight date vs discount date
      const discount = this.items[this.activeButtonIndex];

      const flightDate = new Date(this.selectedFlight.flightInfo.departure_time);
      
      if (flightDate >= discount.startDate && flightDate <= discount.endDate) {
        oneTicketPrice = oneTicketPrice * (1 - discount.discountFactor);
      }

      console.log(oneTicketPrice)

      const ticketPrice = oneTicketPrice * this.passengerCount * (1 - this.items[this.activeButtonIndex].discountFactor);
      const mealsPrice = this.externalServices.meals.reduce((sum, meal) => sum + meal.quantity * meal.price, 0);
      const luggagePrice = this.calculatePrice(this.selectedWeight);

      return ticketPrice + mealsPrice + luggagePrice;
    }

  },

  methods: {
    toggleOverlay(isActive) {
      const overlay = document.querySelector(".overlay");
      if (isActive) {
        document.body.classList.add("modal-active");
        overlay.classList.add("active");
      } else {
        document.body.classList.remove("modal-active");
        overlay.classList.remove("active");
      }
    },
    // Hàm khởi tạo trạng thái ghế
    initializeSeats(class_name) {
      const newSeats = {}; // fix this
      const maxBusinessRow = (this.selectedFlight.flightInfo.aircraft_id === 1) ? 3 : 4;
      [...this.topRows, ...this.bottomRows].forEach((row) => {
        this.seatColumns.forEach((column) => {
          const seatName = `${column}${row}`;
          let isBooked = false;
          if (column >= 1 && column <= maxBusinessRow && (row == "C" || row == "E")) {
            isBooked = true;
          }
          newSeats[seatName] = { isBooked: isBooked, seatID: null }; // default seat_id is null
        });
      });

      this.selectedFlight.seats.forEach((seat) => {
        if (seat.is_available === false || seat.seats.class_name !== class_name) {
          newSeats[seat.seats.seat_number].isBooked = true;
        } else {
          newSeats[seat.seats.seat_number].seatID = seat.seat_id;
        }
      });

      this.seats = newSeats;
    },
    initializePassengers() {
      const first_fake_passengers = {
        first_name: faker.person.firstName(),
        last_name: faker.person.lastName(),
        email: faker.internet.email(),
        gender: faker.helpers.arrayElement(['MALE', 'FEMALE']),
        phone: faker.helpers.replaceSymbols('+##########'), // Generates +1234567890
        birthday: faker.date.birthdate({ min: 18, max: 80, mode: 'age' }).toISOString().split('T')[0], // YYYY-MM-DD format
        seat_id: -1
      }
      console.log(first_fake_passengers)
      this.booking.passengers.push(first_fake_passengers);
    },
    // Hàm lấy style ghế
    getSeatStyle(column, row, isBooked) {
      const seatName = `${column}${row}`;
      if (isBooked === true) {
        return { backgroundColor: "gray", cursor: "not-allowed" }; // Ghế đã đặt
      } else if (this.selectedSeats.some(seat => seat.id === this.seats[seatName].seatID)) {
        return { backgroundColor: "green" }; // Ghế đã chọn
      } else if (column >= 1 && column <= 3) {
        if (row === "C" || row === "E") {
          return { backgroundColor: "gray", cursor: "not-allowed" }; // Ghế Business
        } else {
          return { backgroundColor: "#D1495B" }; // Ghế Business
        }
      } else {
        return { backgroundColor: "#243B4A" }; // Ghế Economy
      }
    },
    // Hàm cập nhật vị trí (place) cho hành khách
    updatePassengerPlace() {
      this.booking.passengers.forEach((passenger, index) => {
        passenger.seat_id = this.selectedSeats[index]?.id || null; // Gán tên ghế hoặc rỗng
        passenger.place = this.selectedSeats[index]?.place || null; // Gán tên ghế hoặc rỗng
      });
    },
    // Update passengers list when count changes
    updatePassengers() {
      const currentCount = this.booking.passengers.length;
      if (this.passengerCount > currentCount) {
        // Add new passengers if count increases
        for (let i = currentCount; i < this.passengerCount; i++) {
          this.booking.passengers.push({
            first_name: faker.person.firstName(),
            last_name: faker.person.lastName(),
            email: faker.internet.email(),
            gender: faker.helpers.arrayElement(['MALE', 'FEMALE']),
            phone: faker.helpers.replaceSymbols('+##########'), // Generates +1234567890
            birthday: faker.date.birthdate({ min: 18, max: 80, mode: 'age' }).toISOString().split('T')[0], // YYYY-MM-DD format
            seat_id: null,
            place: null
          }); // add more fake information
        }
      } else if (this.passengerCount < currentCount) {
        // Remove passengers if count decreases
        this.booking.passengers.splice(this.passengerCount);
      }
    },
    toggleSeatSelection(seatName) {
      if (this.seats[seatName].isBooked === true) return; // Ghế đã đặt

      const seatIndex = this.selectedSeats.findIndex(seat => seat.place === seatName);

      if (seatIndex !== -1) {
        // Hủy chọn
        this.selectedSeats.splice(seatIndex, 1);
      } else if (this.selectedSeats.length < this.passengerCount) {
        // Chọn thêm ghế
        this.selectedSeats.push({ id: this.seats[seatName].seatID, place: seatName });
      }
      this.updatePassengerPlace();
    },
    async updateToOptions() {
      if (!this.airports.departureAirport.id) return;

      try {
        // Fetch possible "To" options based on selected "From"
        const response = await apiClient.get(`/airports/${this.airports.departureAirport.id}/get_arrival_airports`);
        this.airports.toOptions = response.data.data;

        // Clear "To" selection if it's no longer valid
        if (this.airports.arrivalAirport && !this.airports.toOptions.find(option => option.id === this.airports.arrivalAirport.id)) {
          this.airports.arrivalAirport = null;
        }
      } catch (error) {
        this.$toastr.error("Error fetching arrival airports. Please try again.");
      }
    },
    async createBooking() {

      // calculate services used
      this.externalServices.meals.forEach((meal) => {
        if (meal.quantity > 0) {
          this.externalServiceCount.push({ service_id: meal.id, quantity: meal.quantity });
        }
      });
      if (this.selectedWeight > 0) {
        this.externalServiceCount.push({ service_id: this.externalServices.luggageService.id, quantity: this.selectedWeight });
      }

      // create booking with information
      const payload = {
        user_id: this.user.id,
        flight_id: this.selectedFlight.flightInfo.id,
        booking_status: "CONFIRMED",
        passengers: this.booking.passengers,
        class_name: this.selectedClass,
        trip_type: "ONE_WAY",
        services: this.externalServiceCount
      }

      console.log(payload)

      const response = await apiClient.post(`/bookings`, payload);

      if (response.status === 200) {

        // Add booking to store if data is already cached
        this.$toastr.success("Booking created successfully!");
      } else {
        this.$toastr.error("Error creating booking. Please try again.");
        return
      }

      this.isService = false;
      this.isSearched = false;
      //this.searchFlights = null;
    },
    async searchFlights() {
      this.loading = true;

      // validate input
      if (!this.airports.departureAirport || !this.airports.arrivalAirport) {
        this.$toastr.error("Please select departure and arrival airports.");
        this.loading = false; // Tắt loading ngay khi có lỗi
        return;
      }

      if (!this.$refs["checkInDate"].value) {
        this.$toastr.error("Please select a departure date.");
        this.loading = false; // Tắt loading ngay khi có lỗi
        return;
      }

      try {
        const iso_date = new Date(this.$refs["checkInDate"].value).toISOString();

        // get all valid flights based on selected options and departure_date
        const response = await apiClient.get(
          `/flights/search?departure_airport_id=${this.airports.departureAirport.id}&arrival_airport_id=${this.airports.arrivalAirport.id}&departure_date=${iso_date}`
        );

        this.flights = response.data.data.map((flight) => ({
          ...flight,
          formattedDepartureTime: this.formatDate(flight.checkin),
          formattedArrivalTime: this.formatDate(flight.checkout),
        }));

        this.isSearched = true;
      } catch (error) {
        this.$toastr.error("Failed to fetch flights. Please try again.");
      } finally {
        this.loading = false; // Tắt loading ngay sau khi hoàn tất
      }
    },

    async selectFlight(flight, class_name) {
      this.selectedFlight.flightInfo = flight; // Cập nhật chuyến bay được chọn
      // get available seats for selected flight
      const response = await apiClient.get(`/flights/${flight.id}/seats`);
      this.selectedFlight.seats = response.data.data;
      console.log(this.selectedFlight.seats);

      if (class_name === 'ECONOMY') {
        this.isEconomyChoosed = true;
      } else {
        this.isBussinessChoosed = true;
      }
      this.initializeSeats(class_name);
      this.initializePassengers();
      this.isService = true;
      this.isChoosed = true;
      this.selectedClass = class_name;
    },

    undoFlight() {
      this.selectedFlight.flightInfo = null;
      this.selectedFlight.seats = [];
      this.isEconomyChoosed = false;
      this.booking.passengers = [];
      this.selectedSeats = [];
      this.passengerCount = 1;
      this.selectedClass = null;
      this.isBussinessChoosed = false;
      this.isService = false;
      this.isChoosed = false;
    },

    handleDateChange(refName) {
      // Lấy giá trị từ ref dựa trên tên ref
      const inputDate = this.$refs[refName].value;
      this.formattedDates[refName === 'checkInDate' ? 'checkIn' : 'checkOut'] = this.formatDate(inputDate);
    },
    formatDate(inputDate) {
      this.toggleOverlay(false);
      // Chuyển đổi định dạng ngày
      const date = new Date(inputDate);
      const options = { weekday: 'short', day: 'numeric', month: 'short' };
      return date.toLocaleDateString('en-US', options);
    },

    startDragging() {
      this.dragging = true;
      window.addEventListener("mousemove", this.onDrag);
      window.addEventListener("mouseup", this.stopDragging);
    },
    onDrag(event) {
      if (!this.dragging) return;

      const slider = this.$el.querySelector(".slider-container");
      const sliderRect = slider.getBoundingClientRect();
      const offsetX = event.clientX - sliderRect.left;
      const percentage = Math.max(0, Math.min(offsetX / sliderRect.width, 1));
      this.selectedWeight = Math.round(percentage * this.maxWeight);
    },
    stopDragging() {
      this.dragging = false;
      window.removeEventListener("mousemove", this.onDrag);
      window.removeEventListener("mouseup", this.stopDragging);
    },

    calculatePrice(weight) {
      return weight * this.externalServices.luggageService.price; // Tính giá tiền dựa trên số kg
    },

    showSlide(index) {
      if (index >= this.items.length) {
        this.currentIndex = 0;
      } else if (index < 0) {
        this.currentIndex = this.items.length - 1;
      } else {
        this.currentIndex = index;
      }
    },

    prevSlide() {
      this.showSlide(this.currentIndex - 1);
    },

    nextSlide() {
      this.showSlide(this.currentIndex + 1);
    },
    async handleRemoveDiscountClick(index) {
      // Show confirmation dialog
      const confirmDelete = window.confirm("Are you sure you want to delete this discount?");
      if (!confirmDelete) {
        return; // User canceled the action
      }

      // Send delete request
      try {
        const response = await apiClient.delete(`/discounts/${this.items[index].id}`);
        if (response.status === 200) {
          this.items.splice(index, 1);
          this.$toastr.success("Discount removed successfully!");
        } else {
          this.$toastr.error("Error removing discount. Please try again.");
        }
      } catch (error) {
        this.$toastr.error("An error occurred while connecting to the server.");
      }
    },

    handleDiscountButtonClick(index) {
      if (this.activeButtonIndex === index) {
        // Nếu bấm lại vào nút đã chọn, bỏ chọn nút
        this.activeButtonIndex = null;
      } else {
        // Nếu bấm vào nút khác, đổi trạng thái nút
        this.activeButtonIndex = index;
        this.showSlide(index);
      }
    }
  },
  mounted() {
    // Tự động chuyển slide mỗi 5 giây
    setInterval(() => {
      this.nextSlide();
    }, 5000);
    const inputFields = document.querySelectorAll(".typeIn");
    inputFields.forEach((field) => {
      field.addEventListener("focus", () => this.toggleOverlay(true));
      field.addEventListener("blur", () => this.toggleOverlay(false));
    });
  }
};
</script>

<style scoped>
.bookingflexcontainer {
  align-items: center;
  text-align: center;
  gap: 0.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: 100%;
  overflow-x: hidden;
}

.slogan {
  font-family: 'Pacifico', cursive;
  /* Sử dụng Pacifico */
  font-weight: normal;
  /* Không cần in đậm vì font đã có kiểu chữ đẹp */
  font-size: 30px;
  /* Kích thước chữ */
  line-height: 2rem;
  /* Khoảng cách dòng */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  /* Đổ bóng chữ */
  font-style: italic;
  /* Để chữ in nghiêng */
  margin-bottom: 0px;
  margin-top: 13px;
}



.bookingfaceflex {
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-radius: 5rem;
  margin-bottom: 20px;
}

.videoD {
  width: 90%;
  /* Giữ 100% để video chiếm toàn bộ chiều rộng */
  display: flex;
  /* Thêm flexbox cho videoD để căn giữa video */
  justify-content: center;
  /* Căn giữa video theo chiều ngang */
  align-items: center;
  /* Căn giữa video theo chiều dọc nếu có chiều cao */
  height: 260px;
}

.video {
  border-radius: 15rem;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.planeimage {
  position: absolute;
  width: 80%;
  top: -20%;
  height: 300px;
}

.flight-search-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 12px;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 70%;
  z-index: 1000;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.input-field {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  font-size: 0.9rem;
  gap: 5px;
  width: 70%;
}

.input-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 30%;
  background-color: #f5f7f9;
  margin: 0;
  padding: 0;
}

.ticket-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 80px;
  height: 115px;
  border-radius: 30%;
  margin-left: 5px;
  padding: 0;
  overflow: hidden;
  /* Đảm bảo nội dung không vượt khỏi khung */
}

.input-type {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 0.9rem;
  justify-content: center;
  height: 60px;
}

.input-field label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
}

.input-field input {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem;
  margin-top: 0.2rem;
  font-size: 1rem;
  width: 100%;
}

.takeOff {
  width: 95%;
  /* Chiếm toàn bộ chiều rộng của .ticket-icon */
  height: 95%;
  /* Chiếm toàn bộ chiều cao của .ticket-icon */
  object-fit: cover;
  /* Giữ tỷ lệ hình ảnh và lấp đầy khung */
  border-radius: inherit;
  /* Giữ kiểu bo tròn giống .ticket-icon */
  margin: 0;
  padding: 0;
  border: none;
  /* Loại bỏ viền nếu không cần thiết */
  object-fit: contain;
  /* Đảm bảo hình ảnh hiển thị đầy đủ */
}

.fromToImage {
  width: 20px !important;
  /* Chiều rộng của hình ảnh */
  height: 20px;
  /* Chiều cao của hình ảnh */
  /* Tạo hình tròn */
  background-color: #f5f7f9;
  /* Màu nền tương tự ảnh mẫu */
  display: flex;
  justify-content: center;
  align-items: center;
  object-fit: cover;
  /* Đảm bảo hình ảnh hiển thị đầy đủ */
  /* Viền nhạt bao quanh */
  max-width: 20px;
  max-height: 20px;
  margin: 0;
  padding: 0;
}

.search-btn {
  background: linear-gradient(135deg, #003D5B, #00577A);
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 20px;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #1F7D8C;
}

.large-label {
  font-size: 20px;
  font-weight: bold;
}

.typeIn {
  border: none !important;
  outline: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.flight-list {
  width: 100%;
  padding: 20px;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 10px !important;
}

.myheader {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 10px !important;
  font-family: "Arial", sans-serif;
}

.flight-card {
  width: 100%;
  border: 4px solid transparent;
  /* padding: 20px; */
  border-radius: 10px;
  margin-bottom: 30px;
  display: flex;
  flex-direction: row;
  gap: 5px;
  min-width: 800px;
  max-width: fit-content;
  background: linear-gradient(white, white) padding-box,
    linear-gradient(90deg, #003D5B, #1F7D8B) border-box;
}




.price-info {
  display: flex;
  justify-content: center;
  height: 120px;
  align-items: center;
  flex-direction: row;
  margin-left: 20px;
}

.total-price-info {
  display: flex;
  justify-content: center;
  height: 40%;
  align-items: center;
  flex-direction: column;
  margin-left: 40px;
}

.price {
  font-size: 1.8em;
  font-weight: bold;
  color: red;
}

.price-economy {
  font-size: 1.2em;
  font-weight: bold;
  color: white;
}

.price-bussiness {
  font-size: 1.2em;
  font-weight: bold;
  color: black;
}

.select-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #003D5B, #00577A);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  height: 100%;
}

.select-button-economy {
  position: relative;
  padding: 10px 20px;
  background-color: #243B4A;
  color: white;
  border: black;
  cursor: pointer;
  height: 100%;
  width: 130px;
}

.select-button-bussiness {
  position: relative;
  padding: 10px 20px;
  background-color: #D1495B;
  color: black;
  border: black;
  cursor: pointer;
  height: 100%;
  width: 130px;
}

.select-button-bussiness:hover {
  background-color: #B13A4A;
}

.select-button:hover {
  background-color: #1F7D8C;
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

.service-container {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  margin: 30px;
}

.meal-list {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.meal-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 200px;
  border: 2px solid #003D5B;
  /* #003D5B, #1F7D8B */
  border-radius: 8px;
  padding: 10px;
}

.meal-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 10px;
}

.meal-description {
  margin-bottom: 10px;
}

.meal-quantity {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: auto;
}

.meal-quantity button {
  background-color: #377fcd;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 16px;
}

.meal-quantity input {
  width: 50px;
  text-align: center;
  margin: 0 10px;
  font-size: 16px;
}

.input-quantity {
  width: 50px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border: 2px solid #ccc;
  /* Viền cơ bản */
  border-radius: 5px;
  /* Bo góc */
  box-sizing: border-box;
  /* Bao gồm padding và viền trong kích thước */
  margin: 0 10px;
  /* Khoảng cách hai bên */
  background-color: #f9f9f9;
  /* Màu nền nhạt */
  font-size: 16px;
  /* Kích thước chữ lớn hơn */
  color: #333;
  /* Màu chữ đậm */
  transition: all 0.3s ease;
  /* Hiệu ứng mượt mà khi hover */
}

.input-quantity:focus,
.input-quantity:hover {
  border-color: #007bff;
  /* Màu viền khi hover/focus */
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
  /* Hiệu ứng đổ bóng */
  background-color: #e9f5ff;
  /* Màu nền sáng hơn */
  outline: none;
  /* Loại bỏ viền mặc định khi focus */
}

.time {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 60px;
}

.headerInfo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-right: 40px;
}

.arivalTime,
.departureTime,
.airlineText {
  font-weight: bold;
  font-size: 1.1em;
}

.dateConvert,
.flightnumber {
  font-size: 1.0em;
}

.ticket-tour {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
  color: #555;
  width: 600px;
  justify-content: center;
  margin-left: 20px;
  margin-right: 20px;
}

.icons {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 300px;
  margin-bottom: 8px;
}

.icon {
  width: 20px;
  height: 20px;
}

.duration {
  font-size: 14px;
  font-weight: 400;
}

.time2 {
  font-weight: bold;
  color: #000;
}

.progress-bar {
  position: relative;
  width: 100%;
  min-width: 500px;
  height: 8px;
  /* Tăng chiều cao để rõ nét hơn */
  background-color: #e8e8e8;
  /* Màu nền xám nhạt cho line */
  border-radius: 4px;
  /* Bo tròn line */
  margin-bottom: 16px;
  /* Tăng khoảng cách bên dưới */
}

.line {
  position: absolute;
  top: 50%;
  /* Căn giữa theo chiều dọc */
  left: 0;
  width: 100%;
  height: 4px;
  /* Line nhỏ hơn nền */
  background-color: #003D5B;
  /* Màu line đồng bộ với màu nút */
  transform: translateY(-50%);
  /* Căn giữa */
  border-radius: 4px;
  /* Bo tròn line */
  z-index: 1;
}

.circle {
  position: absolute;
  top: 50%;
  /* Căn giữa theo chiều dọc */
  width: 16px;
  /* Kích thước hình tròn */
  height: 16px;
  /* Hình tròn hoàn hảo */
  border-radius: 50%;
  background-color: white;
  /* Màu nền trắng để phù hợp với trang */
  border: 4px solid #003D5B;
  /* Viền xanh đậm đồng bộ với nút */
  box-shadow: 0 0 10px rgba(0, 61, 91, 0.5);
  /* Ánh sáng nhẹ màu xanh đậm */
  transform: translateY(-50%);
  /* Căn giữa */
  z-index: 2;
  transition: background-color 0.3s ease, transform 0.3s ease;
  /* Hiệu ứng hover */
}

.circle.left {
  left: 0;
}

.circle.right {
  right: 0;
}

.labels {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 300px;
  font-size: 14px;
  color: #555;
}

.label {
  text-align: center;
}

.B {
  font-weight: bold;
}

.baggage-slider {
  width: 500px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  text-align: center;
  display: flex;
  flex-direction: column;
}

.slider-container {
  position: relative;
  width: 100%;
  height: 10px;
  background-color: #d3d3d3;
  border-radius: 5px;
}

.track {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #e0e0e0;
  border-radius: 5px;
}

.filled {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #ef325e;
  /* Màu xanh dương */
  border-radius: 5px;
  z-index: 1;
}

.thumb {
  position: absolute;
  top: -15px;
  width: 40px;
  height: 40px;
  transform: translateX(-50%);
  cursor: grab;
  z-index: 2;
}

.thumb:active {
  cursor: grabbing;
}

.luggage-icon {
  width: 100%;
  height: 100%;
  user-select: none;
  /* Ngăn người dùng chọn ảnh */
}

.weight-display {
  margin-top: 20px;
  font-size: 16px;
  font-weight: bold;
  color: red;
}

.image-slider-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 60px;
  overflow: hidden;
  border-radius: 10px;
}

.image-slider {
  display: flex;
  transition: transform 0.5s ease;
}

.slider-item {
  position: relative;
  min-width: 100%;
}

.slider-item img {
  width: 100%;
  height: 300px;
  border-radius: 10px;
  object-fit: cover
}

.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
}

.prev-btn {
  left: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 15px;
  font-size: 24px;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.next-btn {
  right: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 15px;
  font-size: 24px;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.image-slider-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 50px;
  overflow: visible;
  /* Đảm bảo các nút không bị cắt */
  border-radius: 10px;
}

.discount-buttons {
  position: absolute;
  bottom: -40px;
  /* Đẩy nửa dưới nút ra ngoài ảnh */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  z-index: 2;
  /* Đảm bảo các nút không bị che */
}

.discount-buttons-admin {
  position: absolute;
  bottom: -90px;
  /* Đẩy nửa dưới nút ra ngoài ảnh */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  z-index: 2;
  /* Đảm bảo các nút không bị che */
}

.discount-button {
  position: relative;
  width: 200px;
  /* Đặt chiều rộng cố định để các nút đều nhau */
  padding: 10px 0;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  color: #003D5B;
  background-color: white;
  border: 2px solid #003D5B;
  border-radius: 5px;
  cursor: pointer;
  overflow: hidden;
  transition: color 0.4s ease, background-color 0.4s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* Hiệu ứng đổ bóng */
}

.discount-button:hover,
.discount-button:active {
  background-color: #003D5B;
  color: white;
}

.discount-button.active {
  background-color: #003D5B;
  /* Giữ màu sau khi bấm */
  color: white;
}

.discount-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg,
      rgba(255, 255, 255, 0.5),
      rgba(255, 255, 255, 0.1),
      transparent);
  transform: skewX(-45deg);
  z-index: 1;
  transition: all 0.4s ease;
}

.discount-button:hover::before {
  left: 100%;
  /* Ánh sáng lướt từ trái sang phải */
  transition: left 0.6s ease-out;
}

.luggage-finish {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.icon-ticket {
  position: absolute;
  /* Định vị icon */
  top: 10px;
  /* Khoảng cách từ đỉnh nút */
  right: 10px;
  /* Khoảng cách từ bên phải nút */
}

.icon-ticket-image {
  width: 20px;
  /* Độ rộng của logo */
  height: 20px;
  /* Chiều cao của logo */
  object-fit: contain;
  /* Đảm bảo logo không bị méo */

}

.Undo {
  font-size: 1.5rem;
}

.seat-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  /* background-color: #ccc; */
}

.seat-row {
  display: flex;
  align-items: center;
  margin: 1px 0;
  /* Khoảng cách giữa các hàng */
}

.row-label {
  width: 20px;
  /* Hiển thị ký hiệu hàng */
  text-align: center;
  font-weight: bold;
}

.seat-container {
  margin: 1px;
  /* Khoảng cách giữa các ghế */
}

.seat {
  width: 30px;
  height: 30px;
  border: none;
  background-color: transparent;
  /* Nền nút trong suốt */
  border-radius: 5px;
}


.seat.booked {
  background-color: gray;
  cursor: not-allowed;
}

.numbers .number {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin: 1px;
}

.seat-choosing {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  border: 4px solid;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  justify-content: center;
}

.seat-choose-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 50%;
  height: 260px;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
}

#passenger-count {
  width: 60px;
  padding: 0.3rem;
  margin-left: 0.5rem;
}

.passenger-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-radius: 10px;
}

.passenger-card {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  width: 430px;
}

.passenger-card input {
  width: 40px;
  padding: 0.3rem;
  text-align: center;
}

.passenger-numbers-row {
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  margin-bottom: 5px;
}

.seat-status-info {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: auto;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-box {
  width: 20px;
  height: 20px;
  border: 1px solid #000;
}

.seatImage {
  width: 30%;
  /* Chiều rộng chiếm toàn bộ phần tử cha */
  max-width: 205px;
  /* Giới hạn kích thước tối đa */
  height: auto;
  /* Giữ tỉ lệ ảnh */
  object-fit: contain;
  /* Đảm bảo toàn bộ ảnh được hiển thị */
  border-radius: 8px;
  /* Bo tròn nhẹ các góc */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* Hiệu ứng đổ bóng mềm */
  margin: 20px auto;
  /* Căn giữa và tạo khoảng cách */
  display: block;
  /* Đảm bảo căn giữa nếu dùng margin auto */
  border: 2px solid #ddd;
  /* Viền màu nhạt */
  background-color: #f9f9f9;
  /* Màu nền nhẹ nếu ảnh không load */
}

.seat.selected {
  background-color: green !important;
}

.title {
  font-weight: 700;
  font-size: 2rem;
  margin-bottom: 0.8rem;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  /* Khoảng cách giữa các nút */
}

.circle-button {
  text-align: center;
  font-size: 40px;
  margin-top: 5px;
  /* Đảm bảo khoảng cách giữa nút chính và nút tròn */
  width: 40px;
  height: 40px;
  background-color: #003D5B;
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.4s ease, transform 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.circle-button:hover {
  background-color: #002940;
  transform: scale(1.1);
}

.circle-button i {
  font-size: 16px;
}

.remove-discount-icon {
  width: 20px;
  height: 20px;
}

body.modal-active {
  overflow: hidden;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 999;
  display: none;
}

.overlay.active {
  display: block;
}

select.typeIn {
  max-height: 200px;
  /* Hiển thị tối đa 5 mục */
  overflow-y: auto;
}

select[type="dropdown"] option {
  padding: 8px;
}
</style>
