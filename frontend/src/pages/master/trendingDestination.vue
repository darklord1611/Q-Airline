<template>
    <div class="tourist-destinations">
        <h1 class="title">Trending Tourist Destinations</h1>
        <div class="destinations-grid">
            <div v-for="(destination, index) in destinations" :key="index" class="destination-card"
                @click="goToLink(destination.link)">
                <div class="image-container">
                    <img :src="destination.image" :alt="destination.name" />
                    <div class="overlay">
                        <div class="info">
                            <h2>{{ destination.name }}</h2>
                            <p>{{ destination.description }}</p>
                            <p>{{ destination.economy }}</p>
                        </div>
                        <button class="discover-btn">Discover</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import dubaiImg from '@/assets/dubai.jpg';
import newYorkImg from '@/assets/newYork.jpg';
import singaporeImg from '@/assets/sing.jpg';
import tokyoImg from '@/assets/tokyo.jpg';
import parisImg from '@/assets/paris.jpg';
export default {
    name: "TouristDestinations",
    data() {
        return {
            destinations: [
                {
                    name: "Dubai",
                    description: "A futuristic city with stunning architecture and vibrant nightlife.",
                    link: "https://www.visitdubai.com",
                    economy: "Economy from 300 USD",
                    image: dubaiImg // Add image URL here
                },
                {
                    name: "New York",
                    description: "The city that never sleeps, full of iconic landmarks.",
                    link: "https://www.nycgo.com",
                    economy: "Economy from 250 USD",
                    image: newYorkImg // Add image URL here
                },
                {
                    name: "Singapore",
                    description: "A modern city with lush greenery and a blend of cultures.",
                    link: "https://www.visitsingapore.com",
                    economy: "Economy from 200 USD",
                    image: singaporeImg // Add image URL here
                },
                {
                    name: "Tokyo",
                    description: "A bustling metropolis that blends tradition with innovation.",
                    link: "https://www.gotokyo.org",
                    economy: "Economy from 400 USD",
                    image: tokyoImg  // Add image URL here
                },
                {
                    name: "Paris",
                    description: "The city of love, known for its art, fashion, and cuisine.",
                    link: "https://en.parisinfo.com",
                    economy: "Economy from 350 USD",
                    image: parisImg // Add image URL here
                }
            ]
        };
    },
    methods: {
        goToLink(url) {
            window.open(url, "_blank");
        }
    }
};
</script>

<style scoped>
.tourist-destinations {
    text-align: center;
}

.title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.destinations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.destination-card {
    position: relative;
    cursor: pointer;
    overflow: hidden;
    border-radius: 10px;
    transition: transform 0.3s;
}

.destination-card:hover {
    transform: scale(1.05);
}

.image-container {
    position: relative;
}

.image-container img {
    width: 100%;
    height: 100%;
    max-height: 600px;
    display: block;
    border-radius: 10px;
    transition: opacity 0.3s;
}

.image-container .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    opacity: 0;
    transition: opacity 0.3s;
    padding: 1rem;
}

.image-container:hover .overlay {
    opacity: 1;
}

.image-container .info {
    text-align: left;
}

.image-container h2 {
    font-size: 1.5rem;
    margin: 0;
}

.image-container p {
    margin: 0.5rem 0;
}

.discover-btn {
    align-self: center;
    padding: 0.5rem 1rem;
    background-color: #D1495B;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.discover-btn:hover {
    background-color: #B13A4A;
}
</style>