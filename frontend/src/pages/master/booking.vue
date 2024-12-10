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

    <div class="flight-search-container">
      <div class="class-selection">
        <button class="class-option" v-for="(option, index) in classOptions" :key="index"
          :class="{ active: selectedClass === option }" @click="selectedClass = option">
          {{ option }}
        </button>
      </div>

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
        <div class="input-field">
          <div class="input-icon">
            <img :src="calendar" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">
              Check In
            </label>
            <input type="date" ref="checkInDate" @change="handleDateChange('checkInDate')" class="typeIn" />
          </div>
        </div>
        <div class="input-field">
          <div class="input-icon">
            <img :src="calendar" class="fromToImage" />
          </div>
          <div class="input-type">
            <label class="large-label">
              Check Out
            </label>
            <input type="date" ref="checkOutDate" @change="handleDateChange('checkOutDate')" class="typeIn" />
          </div>
        </div>
        <button class="search-btn" @click="searchFlights">Search Flight</button>
      </div>
    </div>

    <div class="image-slider-container">
      <button @click="prevSlide" class="prev-btn">&#10094;</button>
      <div class="image-slider">
        <div class="slider-item" v-for="(item, index) in items" :key="index" v-show="currentIndex === index">
          <img :src="item.image" :alt="'Image ' + (index + 1)">
          <div class="text-overlay">{{ item.text }}</div>
          <div class="discount-buttons">
            <button class="discount-button" :class="{ active: activeButtonIndex === 0 }"
              @click="handleDiscountButtonClick(0)">NewYork Traveling</button>
            <button class="discount-button" :class="{ active: activeButtonIndex === 1 }"
              @click="handleDiscountButtonClick(1)">Tet Homecoming Flight</button>
            <button class="discount-button" :class="{ active: activeButtonIndex === 2 }"
              @click="handleDiscountButtonClick(2)">Southeast Asia Traveling</button>
          </div>
        </div>
      </div>
      <button @click="nextSlide" class="next-btn">&#10095;</button>
    </div>



    <div class="flight-list" v-if="isSearched">
      <label class="myheader">Available Flights</label>
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
          <div class="dateConvert"> {{ formattedDates.checkIn }}</div>
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
          <div class="dateConvert"> {{ formattedDates.checkOut }}</div>
        </div>
        <!-- Thông tin giá và nút chọn -->
        <div class="price-info">
          <span class="price">${{ flight.class_pricing[0].base_price }} USD</span>
          <button class="select-button" v-if="!isChoosed" @click="selectFlight(flight)">Booking Now!</button>
          <button class="select-button" v-if="isChoosed" @click="undo()">Undo</button>
        </div>
      </div>
    </div>
    <!-- lựa chọn meal -->
    <div class="meal-container" v-if="isService">
      <label class="myheader">Qmeal Service</label>
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
        <label class="myheader">Qluggage Service</label>
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
      <div class="price-info">
        <span class="price">Total: ${{ totalPrice }} USD</span>
        <button class="select-button">Finish!</button>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import video from "@/assets/58475-488682084_small.mp4";
import image from "@/assets/vecteezy_plane-png-with-ai-generated_26773766.png";
import fromTo from "@/assets/pin.png";
import calendar from "@/assets/calendar.png";
import standardMeal from "@/assets/h2-meal.jpg";
import premiumMeal from "@/assets/premium.jpg";
import vegeMeal from "@/assets/vege.jpg";
import kidMeal from "@/assets/kid.jpg";
import tetImage from "@/assets/tet.jpg";
import cityImage from "@/assets/city.jpg";
import dnaImage from "@/assets/dna.jpg";
import Footer from '@/pages/master/footer.vue';

import axios from 'axios';

export default {
  components: {
    Footer
  },
  name: "booking",
  data() {
    return {
      totalPrice: 0,
      selectedWeight: 0, // Giá trị ban đầu của số cân nặng
      maxWeight: 20, // Số cân tối đa
      dragging: false, // Trạng thái kéo
      pricePerKg: 50,
      activeButtonIndex: null,
      formattedDates: {
        checkIn: '',
        checkOut: ''
      },
      video,
      image,
      standardMeal,
      premiumMeal,
      vegeMeal,
      kidMeal,
      fromTo,
      calendar,
      classOptions: ['Economy', 'Business Class'],
      selectedClass: 'Economy',
      isSearched: false,
      isChoosed: false,
      isService: false,
      selectedFlight: null,
      meals: [
        {
          name: 'Standard Meal',
          description: 'A common meal with options like chicken, beef, or fish with rice, mashed potatoes, or pasta.',
          imgSrc: standardMeal,
          quantity: 0,
          price: 50,
        },
        {
          name: 'Premium Meal',
          description: 'A luxurious meal with options like filet mignon, grilled salmon, or lobster with special sauces.',
          imgSrc: premiumMeal,
          quantity: 0,
          price: 90,
        },
        {
          name: 'Vegetarian Meal',
          description: 'A plant-based meal including options like mushroom rice, pasta with lentils, and fresh salads.',
          imgSrc: vegeMeal,
          quantity: 0,
          price: 60
        },
        {
          name: 'Kid Meal',
          description: 'A kid-friendly meal with chicken nuggets, macaroni and cheese, and small sandwiches.',
          imgSrc: kidMeal,
          quantity: 0,
          price: 35,
        }
      ],
      currentIndex: 0,
      items: [
        { image: cityImage, text: 'NewYork Traveling - Discount 30%' },
        { image: tetImage, text: 'Tet Holiday: flight coming home - Discount 50%' },
        { image: dnaImage, text: 'Southeast Aisa Traveling - Discount 40%' }
      ],
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
        luggage: []
      }
    };
  },
  async created() {
    try {
      // Fetch all airports initially
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/airports`);;
      this.airports.defaultOptions = response.data.data;
      this.airports.fromOptions = [...this.airports.defaultOptions];
      this.airports.toOptions = [...this.airports.defaultOptions];
    } catch (error) {
      console.error("Error fetching initial airports:", error);
    }

    try {
      // Fetching external services like meals or luggage
      // Fetch all airports initially
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/services/search?service_type=MEAL`);;
      this.externalServices.meals = response.data.data;
      console.log(this.externalServices.meals);
    } catch(error) {
      console.error("Error fetching external services:", error);
    }

  },

  computed: {
    filteredFlights() {
      if (!this.selectedFlight) return this.flights;
      return this.flights.filter(
        (flight) => flight.flightNumber === this.selectedFlight.flightNumber
      );
    },

    totalPrice() {
      const flightPrice = this.isChoosed && this.selectedFlight ? this.selectedFlight.price : 0;
      const mealsPrice = this.meals.reduce((sum, meal) => sum + meal.quantity * meal.price, 0);
      const luggagePrice = this.calculatePrice(this.selectedWeight);

      return flightPrice + mealsPrice + luggagePrice;
    }

  },

  methods: {
    async updateToOptions() {
      if (!this.airports.departureAirport.id) return;

      try {
        // Fetch possible "To" options based on selected "From"
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/airports/${this.airports.departureAirport.id}/get_arrival_airports`);
        this.airports.toOptions = response.data.data;
        
        // Clear "To" selection if it's no longer valid
        if (this.airports.arrivalAirport && !this.airports.toOptions.find(option => option.id === this.airports.arrivalAirport.id)) {
          this.airports.arrivalAirport = null;
        }
      } catch (error) {
        console.error("Error updating 'To' options:", error);
      }
    },
    // async updateFromOptions() {
    //   if (!this.to) return;

    //   try {
    //     // Fetch possible "From" options based on selected "To"
    //     const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/airports/${this.to}/get_departure_airports`);
    //     this.airports.fromOptions = response.data.data;
        
    //     // Clear "From" selection if it's no longer valid
    //     if (!this.airports.fromOptions.find(option => option.id === this.from)) {
    //       this.from = null;
    //     }
    //   } catch (error) {
    //     console.error("Error updating 'From' options:", error);
    //   }
    // },
    async searchFlights() {

      console.log(this.airports.departureAirport.id);
      console.log(this.airports.arrivalAirport.id);
      console.log(this.$refs["checkInDate"].value)
      const iso_date = new Date(this.$refs["checkInDate"].value).toISOString();
      console.log(iso_date)

      // get all valid flights based on selected options and departure_date
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/flights/search?departure_airport_id=${this.airports.departureAirport.id}&arrival_airport_id=${this.airports.arrivalAirport.id}&departure_date=${iso_date}`);

      this.flights = response.data.data;
      console.log(response.data.data)

      console.log(this.flights);

      this.isSearched = true; // Đặt thành true khi bấm nút Search Flight
    },
    selectFlight(flight) {
      this.selectedFlight = flight; // Cập nhật chuyến bay được chọn
      this.isChoosed = true;
      this.isService = true;
    },

    undo(flight) {
      this.selectedFlight = null;
      this.isChoosed = false;
      this.isService = false;
    },

    handleDateChange(refName) {
      // Lấy giá trị từ ref dựa trên tên ref
      const inputDate = this.$refs[refName].value;
      this.formattedDates[refName === 'checkInDate' ? 'checkIn' : 'checkOut'] = this.formatDate(inputDate);
    },
    formatDate(inputDate) {
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
      return weight * this.pricePerKg; // Tính giá tiền dựa trên số kg
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

    handleDiscountButtonClick(index) {
      if (this.activeButtonIndex === index) {
        // Nếu bấm lại vào nút đã chọn, bỏ chọn nút
        this.activeButtonIndex = null;
      } else {
        // Nếu bấm vào nút khác, đổi trạng thái nút
        this.activeButtonIndex = index;
      }
    }
  },
  mounted() {
    // Tự động chuyển slide mỗi 5 giây
    setInterval(() => {
      this.nextSlide();
    }, 5000);
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
  font-size: 40px;
  /* Kích thước chữ */
  line-height: 2rem;
  /* Khoảng cách dòng */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  /* Đổ bóng chữ */
  font-style: italic;
  /* Để chữ in nghiêng */
  margin-bottom: 20px;
  margin-top: 20px;
}



.bookingfaceflex {
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-radius: 5rem;
  margin-bottom: 10px;
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
  height: 300px;
}

.video {
  border-radius: 15rem;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.planeimage {
  position: absolute;
  width: 85%;
  top: -12%;
  height: 300px;
}

.flight-search-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.class-selection {
  display: flex;
  justify-content: center;
  /* Các nút nằm sát nhau */
  align-items: center;
  /* Căn giữa theo chiều dọc */
  padding: 10px 0;
  /* Khoảng cách trên dưới */
}

.class-option {
  padding: 10px 20px;
  /* Khoảng cách bên trong nút */
  border: none;
  /* Loại bỏ viền */
  background-color: #4CB5D2;
  /* Màu nền cho nút */
  border-radius: 4px;
  /* Bo tròn nút */
  cursor: pointer;
  /* Hiển thị con trỏ khi hover */
  transition: background-color 0.3s, transform 0.2s;
  /* Hiệu ứng hover */
  margin-right: 0;
  /* Loại bỏ khoảng cách phải giữa các nút */
  color: white;
}

.class-option:last-child {
  margin-right: 0;
  /* Đảm bảo nút cuối không có margin phải */
}

.class-option.active {
  background-color: #003D5B;
  /* Màu cho nút đang chọn */
  font-weight: bold;
  /* Chữ đậm */
}

.class-option:hover {
  background-color: #4CB5D2;
  /* Hiệu ứng hover */
  transform: scale(1.05);
  /* Hiệu ứng phóng to nhẹ */
}



.input-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.input-field {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  font-size: 0.9rem;
  gap: 5px;
  width: 100%;
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
  height: 90px;
  border-radius: 30%;
  margin: 0;
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
  border-radius: 20%;
  /* Tạo hình tròn */
  background-color: #f5f7f9;
  /* Màu nền tương tự ảnh mẫu */
  display: flex;
  justify-content: center;
  align-items: center;
  object-fit: cover;
  /* Đảm bảo hình ảnh hiển thị đầy đủ */
  border: 1px solid #e0e0e0;
  /* Viền nhạt bao quanh */
  max-width: 20px;
  max-height: 20px;
  margin: 0;
  padding: 0;
}

.search-btn {
  background-color: #003D5B;
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
  font-family: 'Merriweather', serif;
}

.flight-card {
  width: 100%;
  border: 4px solid transparent;
  padding: 20px;
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
  width: 100%;
  align-items: center;
  flex-direction: column;
  margin-left: 40px;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: red;
}

.select-button {
  padding: 10px 20px;
  background-color: #003D5B;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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

.meal-container {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
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
  border: 1px solid #ddd;
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
  bottom: -20px;
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
}
</style>
