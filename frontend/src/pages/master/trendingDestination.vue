<template>
    <div class="tourist-destinations">
        <h1 class="title">Trending Tourist Destinations</h1>
        <div class="destinations-grid">
            <div v-for="(destination, index) in destinations" :key="index" class="destination-card">
                <div class="image-container">
                    <img :src="destination.image" :alt="destination.name" />
                    <div class="overlay">
                        <div class="info">
                            <h2>{{ destination.name }}</h2>
                            <p>{{ destination.description }}</p>
                        </div>
                        <div class="button-col">
                            <button class="discover-btn" @click="goToLink(destination.link)">Discover</button>
                            <button class="discover-btn" @click="remove(index)">Remove</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api/axios';
import { useUserStore } from '@/stores/user';

export default {
    name: "TouristDestinations",
    data() {
        return {
            destinations: []
        };
    },
    async created() {
        const response = await apiClient.get('/news/destinations');
        const userStore = useUserStore();
        this.user = userStore.user;
        this.isAdmin = this.user.role === 'admin';

        this.destinations = response.data.data.map((destination) => {
            const aspectRatio = destination.image_height / destination.image_width;
            return {
                id: destination.id,
                name: destination.title,
                description: destination.body,
                link: destination.external_article_link,
                image: destination.image_url,
                aspectRatio: Math.max(aspectRatio || 1, 1) // Avoid overly small ratios
            };
        });
    },
    methods: {
        goToLink(url) {
            window.open(url, "_blank");
        },
        async remove(index) {
            // send request to remove destination

            const response = await apiClient.delete(`/news/${this.destinations[index].id}`);
            if (response.status === 200) {
                this.$toastr.success('Destination removed successfully');
                this.destinations.splice(index, 1);
            } else {
                this.$toastr.error('Failed to remove destination');
            }
        }
    }
};
</script>

<style scoped>
.tourist-destinations {
    text-align: center;
    margin-bottom: 1em;
}

.title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.destinations-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    padding: 1.5rem;
}

.destination-card {
    position: relative;
    cursor: pointer;
    overflow: hidden;
    border-radius: 10px;
    transition: transform 0.3s;
    display: flex;
    flex-direction: column;
    height: 400px;
}

.destination-card:hover {
    transform: scale(1.05);
}

.image-container {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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
    border-radius: 10px;
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

.button-col {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
</style>
