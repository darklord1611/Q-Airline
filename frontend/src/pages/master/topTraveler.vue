<template>
    <div class="best-travelers">
        <h1 class="title">Best travelers of the Month</h1>
        <div class="travelers">
            <div v-for="(traveler, index) in travelers" :key="index" class="traveler-card">
                <img class="city-image" :src="traveler.cityImage" alt="City Image" />
                <img class="avatar" :src="traveler.avatar" alt="Traveler Avatar" />
                <div class="info">
                    <h2 class="name">{{ traveler.name }}</h2>
                    <p class="city">{{ traveler.city }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import img1 from '@/assets/img1.jpg';
import img2 from '@/assets/img2.jpg';
import img3 from '@/assets/img3.jpg';
import img4 from '@/assets/img4.jpg';
import ava1 from '@/assets/ava1.jpg';
import ava2 from '@/assets/ava2.jpg';
import ava3 from '@/assets/ava3.jpg';
import ava4 from '@/assets/ava4.jpg';

export default {
    name: "BestTravelers",
    data() {
        return {
            travelers: [
                {
                    name: "William Lam",
                    city: "Shanghai",
                    cityImage: img1,
                    avatar: ava1,
                },
                {
                    name: "James Nash",
                    city: "Dubai",
                    cityImage: img2,
                    avatar: ava2,
                },
                {
                    name: "Lexi Tushima",
                    city: "Tokyo",
                    cityImage: img3,
                    avatar: ava3,
                },
                {
                    name: "Sebastian John",
                    city: "New York",
                    cityImage: img4,
                    avatar: ava4,
                },
            ],
        };
    },
};
</script>

<style scoped>
.best-travelers {
    text-align: left;
    padding: 20px;
}

.title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.travelers {
    display: flex;
    justify-content: space-between;
    gap: 50px;
}

.traveler-card {
    width: 200px;
    text-align: center;
    position: relative;
}

.city-image {
    width: 85%;
    height: 160px;
    border-top-left-radius: 10rem;
    border-top-right-radius: 10rem;
    object-fit: cover;
}

.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
    position: absolute;
    top: 135px;
    left: 42.5%;
    transform: translateX(-50%);
    z-index: 1;
    animation: float 3s ease-in-out infinite;
    background: linear-gradient(135deg, #ff7eb3, #ff758c, #ffb199);
    background-size: 200% 200%;
    /* animation: gradient 5s ease infinite, float 3s ease-in-out infinite; */
}

/* @keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

@keyframes float {

    0%,
    100% {
        transform: translate(-50%, -5px);
    }

    50% {
        transform: translate(-50%, 5px);
    }
} */

.info {
    width: 85%;
    margin-top: 5px;
    padding: 10px;
    border-bottom-left-radius: 10rem;
    border-bottom-right-radius: 10rem;
    background-color: #f9f9f9;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.name {
    font-size: 16px;
    font-weight: bold;
    margin: 10px 0 5px;
}

.city {
    font-size: 14px;
    color: gray;
}
</style>
