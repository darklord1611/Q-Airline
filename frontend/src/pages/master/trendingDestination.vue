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
                        </div>
                        <button class="discover-btn">Discover</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api/axios';

export default {
    name: "TouristDestinations",
    data() {
        return {
            destinations: []
        };
    },
    async created() {
        // Fetch data from an API and set it to the destinations array
        
        const response = await apiClient.get('/news/destinations');

        console.log(response.data.data);
    
        this.destinations = response.data.data.map(destination => ({
            name: destination.title,
            description: destination.body,
            link: destination.external_article_link,
            image: destination.image_url
        }));

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