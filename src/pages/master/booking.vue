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
                 <button class="class-option" v-for="(option, index) in classOptions" :key="index" :class="{ active: selectedClass === option }" @click="selectedClass = option">
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
            <button class="search-button">Search Flight</button>
        </div>
    </div>
</template>

<script>
    import video from "@/assets/58475-488682084_small.mp4";
    import image from "@/assets/vecteezy_plane-png-with-ai-generated_26773766.png";

    export default {
        data() {
            return {
                video,
                image,
                classOptions: ['Economy', 'Business Class', 'First Class'],
                selectedClass: 'Economy'
            };
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
</style>
