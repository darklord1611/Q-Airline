<template>
    <div class="weather-card">
        <!-- Icon minh họa thời tiết -->
        <div class="weather-icon">
            <img src="@/assets/sun.png" alt="Weather Icon" />
        </div>

        <!-- Thông tin thời tiết -->
        <div class="weather-info">
            <h2 class="location">{{ location }}</h2>
            <p class="date">{{ currentDate }}</p>
            <p class="temperature">{{ temperature }}°C</p>
            <p class="description">{{ weatherDescription }}</p>
        </div>

        <!-- Ảnh của địa điểm -->
        <div class="location-image">
            <img src="@/assets/danang.jpg" alt="Location Image" />
        </div>
    </div>
</template>

<script>
export default {
    name: "WeatherCard",
    data() {
        return {
            location: "Đà Nẵng", // Tên địa điểm
            temperature: 30, // Nhiệt độ
            weatherDescription: "Nắng đẹp", // Mô tả thời tiết
            currentDate: this.getCurrentDate(), // Lấy ngày hiện tại
        };
    },
    methods: {
        getCurrentDate() {
            const options = { weekday: "long", day: "numeric", month: "long", year: "numeric" };
            return new Date().toLocaleDateString("vi-VN", options);
        },
    },
};
</script>

<style scoped>
.weather-card {
    width: 100%;
    background: linear-gradient(135deg, #00577a, #007a99);
    border-radius: 15px;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    color: #fff;
    font-family: "Arial", sans-serif;
    text-align: center;
    position: relative;
}

.weather-icon {
    padding: 15px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.weather-icon img {
    width: 80px;
    height: 80px;
}

.weather-info {
    background: rgba(0, 0, 0, 0.2);
    padding: 15px 10px;
}

.weather-info .location {
    font-size: 1.8em;
    font-weight: bold;
    margin: 5px 0;
}

.weather-info .date {
    font-size: 0.9em;
    margin: 5px 0;
    color: #d1ecf1;
}

.weather-info .temperature {
    font-size: 2.5em;
    font-weight: bold;
    margin: 10px 0;
}

.weather-info .description {
    font-size: 1em;
    font-style: italic;
    margin: 5px 0;
}

.location-image {
    width: 100%;
    height: 200px;
    overflow: hidden;
}

.location-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
</style>