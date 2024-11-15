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
        <button 
          class="class-option" 
          v-for="(option, index) in classOptions" 
          :key="index" 
          :class="{ active: selectedClass === option }" 
          @click="selectedClass = option"
        >
          {{ option }}
        </button>
      </div>

      <div class="input-group">
        <div class="input-field">
          <label>From</label>
          <input type="text" v-model="from" placeholder="Type your location">
        </div>
        <div class="input-field">
          <label>To</label>
          <input type="text" v-model="to" placeholder="Type where do you want to go">
        </div>
        <div class="input-field">
          <label>Check In</label>
          <input type="date" ref="checkInDate" @change="handleDateChange('checkInDate')" />
        </div>
        <div class="input-field">
          <label>Check Out</label>
          <input type="date" ref="checkOutDate" @change="handleDateChange('checkOutDate')" />
        </div>
      </div>
      
      <button class="search-button" @click="searchFlights">Search Flight</button>
    </div>

    <div class="flight-list" v-if="isSearched">
      <h2>Available Flights</h2>
      <div 
  class="flight-card" 
  v-for="flight in flights" 
  :key="flight.flightNumber"
>
<div class="flight-info-horizontal">
  <!-- Cột trái: Thời gian -->
  <div class="time-column">
    <div class="time-block departure-time">
      <span class="time">{{ flight.departureTime }}</span>
      <div class="date">{{ formattedDates.checkIn }}</div>
    </div>
    <div class="spacer"></div>
    <div class="duration"><span>{{ flight.duration }}</span></div>
    <div class="time-block arrival-time">
      <span class="time">{{ flight.arrivalTime }}</span>
      <div class="date">{{ formattedDates.checkOut }}</div>
    </div>
  </div>

  <!-- Cột giữa: Đường bay -->
  <div class="route-column">
    <div class="icon icon-departure">●</div>
    <div class="line"></div>
    <div class="icon icon-plane">
      <img src="@/assets/plane.png" alt="plane icon" />
    </div>
    <div class="line"></div>
    <div class="icon icon-location">
      <img src="@/assets/location-sign.png" alt="location icon" />
    </div>
  </div>

  <!-- Cột phải: Sân bay -->
  <div class="airport-column">
    <div class="airport-block departure-airport">
      <span>{{ flight.departureAirport }}</span>
      <div class="from"> {{ from }}</div>
    </div>
    <div class="spacer"></div>
    <div class="airport-block arrival-airport">
      <span>{{ flight.arrivalAirport }}</span>
      <div class="to"> {{ to }}</div>
    </div>
  </div>

</div>


  <!-- Thông tin giá và nút chọn -->
  <div class="price-info-horizontal">
    <span class="price">USD {{ flight.price }}</span>
    <button class="select-button">Select Flight</button>
  </div>
</div>



    </div>
  </div>
</template>

<script>
import video from "@/assets/58475-488682084_small.mp4";
import image from "@/assets/vecteezy_plane-png-with-ai-generated_26773766.png";

export default {
  name: "booking",
  data() {
    return {
      from: '', // Lưu giá trị của ô "From"
      to: '',    // Lưu giá trị của ô "To"
      formattedDates: {
        checkIn: '',
        checkOut: ''
      },
      video,
      image,
      classOptions: ['Economy', 'Business Class', 'First Class'],
      selectedClass: 'Economy',
      isSearched: false,
      flights: [
        {
          departureAirport: "JFK",
          departureTime: "08:00 AM",
          arrivalAirport: "LAX",
          arrivalTime: "11:30 AM",
          flightNumber: "AA123",
          duration: "5h30m",
          price: "$299"
        },
        {
          departureAirport: "SFO",
          departureTime: "09:15 AM",
          arrivalAirport: "ORD",
          arrivalTime: "03:45 PM",
          flightNumber: "UA456",
          duration: "4h30m",
          price: "$259"
        },
        {
          departureAirport: "LHR",
          departureTime: "02:30 PM",
          arrivalAirport: "DXB",
          arrivalTime: "12:15 AM",
          flightNumber: "EK789",
          duration: "7h45m",
          price: "$599"
        }
      ]
    };
  },
  methods: {
    searchFlights() {
      this.isSearched = true; // Đặt thành true khi bấm nút Search Flight
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
    }  
  }
};
</script>

<style scoped>
  .bookingflexcontainer {
      align-items: center;
      text-align: center;
      gap: 2rem;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
  }

  .slogan {
  font-family: 'Pacifico', cursive; /* Sử dụng Pacifico */
  font-weight: normal; /* Không cần in đậm vì font đã có kiểu chữ đẹp */
  font-size: 40px; /* Kích thước chữ */
  line-height: 2rem; /* Khoảng cách dòng */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Đổ bóng chữ */
  font-style: italic; /* Để chữ in nghiêng */
  }



  .bookingfaceflex {
      width: 90%;
      margin: 1rem auto 0;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      border-radius: 5rem;
  }

  .videoD {
  width: 90%; /* Giữ 100% để video chiếm toàn bộ chiều rộng */
  display: flex; /* Thêm flexbox cho videoD để căn giữa video */
  justify-content: center; /* Căn giữa video theo chiều ngang */
  align-items: center; /* Căn giữa video theo chiều dọc nếu có chiều cao */
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
justify-content: space-around;
}

.class-option {
padding: 10px 20px;
border: none;
background-color: #f0f0f0;
border-radius: 5px;
cursor: pointer;
transition: background-color 0.3s;
}

.class-option.active {
background-color: #007bff;
color: #fff;
}

.class-option:hover {
background-color: #e0e0e0;
}

.input-group {
display: flex;
justify-content: space-between;
gap: 10px;
}

.input-field {
display: flex;
flex-direction: column;
flex: 1;
}

.input-field label {
margin-bottom: 5px;
font-weight: 500;
}

.input-field input {
padding: 8px;
border: 1px solid #ccc;
border-radius: 5px;
}

.search-button {
padding: 10px;
background-color: #007bff;
color: #fff;
border: none;
border-radius: 5px;
cursor: pointer;
font-size: 16px;
transition: background-color 0.3s;
}

.search-button:hover {
background-color: #0056b3;
}

.flight-list {
width: 100%;
margin: auto;
padding: 20px;
font-family: Arial, sans-serif;
display: flex;
flex-direction: column;
gap: 40px;
align-items: center;
}

h2 {
text-align: center;
color: #333;
font-size: 1.8rem;
margin-bottom: 20px;
}

.flight-card {
  width: 100%;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 60px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  max-width: 800px;
  background-image: url(@/assets/bookingbg.jpg); /* Đặt đường dẫn đến ảnh nền */
  background-size: cover; /* Đảm bảo ảnh phủ toàn bộ diện tích của flight-card */
  background-position: center; /* Căn giữa ảnh */
  justify-content: space-between;
}

.flight-info-horizontal {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 200px; /* Chiều cao cố định để dễ căn chỉnh */
  gap: 40px;
}

/* Cột trái: Thời gian */
.time-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Đẩy thời gian lên đầu và xuống cuối */
}

/* Cột giữa: Đường bay */
.route-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.icon-departure,
.icon-arrival {
  font-size: 1.2em;
}

.line {
  width: 2px;
  flex: 1;
  background-color: #ccc;
}

.icon-plane {
  width: 26px;   /* Kích thước nhỏ tùy chọn */
  height: 26px;  /* Kích thước nhỏ tùy chọn */
}

.icon-location {
  margin-top: 10px;
  width: 24px;   /* Kích thước nhỏ tùy chọn */
  height: 24px;  /* Kích thước nhỏ tùy chọn */
}


/* Cột phải: Sân bay */
.airport-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Đẩy tên sân bay lên đầu và xuống cuối */
  align-items: center; /* Căn các phần tử theo chiều ngang */
  height: 100%;
}

/* Các class căn chỉnh cụ thể */
.departure-time,
.departure-airport {
  align-self: flex-start;
}

.arrival-time,
.arrival-airport {
  align-self: flex-end;
  margin: 0;
}

.duration {
  font-size: 1.0em;
  font-weight: bold;
  justify-content: center; 
  margin-top: auto; /* Tạo khoảng trống phía trên, đẩy xuống giữa */
  margin-bottom: auto; /* Tạo khoảng trống phía dưới, giữ ở giữa */
}
/* Kiểu chữ cho thời gian và sân bay */
.time-block {
  font-size: 1.2em;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.airport-block {
  font-size: 1.2em;
  font-weight: bold;
  justify-content: left;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.price-info-horizontal {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: red;
}

.select-button {
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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

</style>
