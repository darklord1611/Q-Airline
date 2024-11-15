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
          <input type="text" placeholder="Type your location">
        </div>
        <div class="input-field">
          <label>To</label>
          <input type="text" placeholder="Type where do you want to go">
        </div>
        <div class="input-field">
          <label>Check In</label>
          <input type="date">
        </div>
        <div class="input-field">
          <label>Check Out</label>
          <input type="date">
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
        <div class="flight-info">
          <div class="flight-time">
            <div class="time">
              <span class="label">Departure Time:</span>
              <span class="value">{{ flight.departureTime }}</span>
            </div>
            <div class="time">
              <span class="label">Arrival Time:</span>
              <span class="value">{{ flight.arrivalTime }}</span>
            </div>
          </div>

          <div class="flight-route">
            <div class="icon icon-departure">●</div>
            <div class="line"></div>
            <div class="icon icon-plane">✈️</div>
            <div class="line"></div>
            <div class="icon icon-arrival">●</div>
          </div>

          <div class="flight-airport">
            <div class="airport">
              <span class="label">Departure Airport:</span>
              <span class="value">{{ flight.departureAirport }}</span>
            </div>
            <div class="airport">
              <span class="label">Arrival Airport:</span>
              <span class="value">{{ flight.arrivalAirport }}</span>
            </div>
          </div>
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
          duration: "5h 30m",
          price: "$299"
        },
        {
          departureAirport: "SFO",
          departureTime: "09:15 AM",
          arrivalAirport: "ORD",
          arrivalTime: "03:45 PM",
          flightNumber: "UA456",
          duration: "4h 30m",
          price: "$259"
        },
        {
          departureAirport: "LHR",
          departureTime: "02:30 PM",
          arrivalAirport: "DXB",
          arrivalTime: "12:15 AM",
          flightNumber: "EK789",
          duration: "7h 45m",
          price: "$599"
        }
      ]
    };
  },
  methods: {
    searchFlights() {
      this.isSearched = true; // Đặt thành true khi bấm nút Search Flight
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
max-width: 800px;
margin: auto;
padding: 20px;
font-family: Arial, sans-serif;
}

h2 {
text-align: center;
color: #333;
font-size: 1.8rem;
margin-bottom: 20px;
}

.flight-card {
background-color: #fff;
border: 1px solid #ddd;
border-radius: 8px;
padding: 20px;
margin-bottom: 15px;
box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
transition: transform 0.2s;
}

.flight-card:hover {
transform: scale(1.02);
}

.flight-info {
display: flex;
flex-wrap: wrap;
gap: 10px 20px;
}

.flight-row {
width: calc(50% - 10px);
display: flex;
justify-content: space-between;
padding: 5px 0;
}

.label {
color: #555;
font-weight: bold;
}

.value {
color: #333;
}

.price {
color: #e63946;
font-size: 1.2rem;
font-weight: bold;
}
</style>
