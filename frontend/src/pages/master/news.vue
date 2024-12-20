<template>
    <div class="travel-news-container">
        <h3 class="travel-heading">{{ heading }}</h3>
        <h1 class="travel-title">{{ title }}</h1>
        <p class="travel-description">{{ description }}</p>
    </div>
    <div class="container">
        <!-- Cột trái: Danh sách thông tin -->
        <div class="info-list">
            <div v-for="(item, index) in visibleItems" :key="index" class="info-card" @click="selectItem(item)">
                <div class="remove-row">
                    <span class="card-number">{{ item.number }}</span>
                    <button v-if="isAdmin" class="circle-button" @click="handleRemoveNewClick(index)">
                        -
                    </button>
                </div>

                <span class="card-title">{{ item.title }}</span>
            </div>
            <!-- Thanh cuốn -->
            <div v-show="items.length > 3" class="scrollbar">
                <button @click="scrollUp">▲</button>
                <button @click="scrollDown">▼</button>
            </div>
        </div>

        <!-- Cột phải: Hiển thị ảnh hoặc tin tức chi tiết -->
        <div class="info-details">
            <div v-if="!selectedItem" class="image-container">
                <img src="@/assets/new1.jpg" alt="Image 1" class="airplane-window image-small" />
                <img src="@/assets/new3.jpg" alt="Image 2" class="airplane-window image-large" />
                <img src="@/assets/new2.jpg" alt="Image 3" class="airplane-window image-smallest" />
            </div>
            <div v-else class="news-details">
                <h2>{{ selectedItem.title }}</h2>
                <p>{{ selectedItem.details }}</p>
            </div>
        </div>
    </div>
</template>

<script>

import apiClient from "@/api/axios";
import { useUserStore } from '@/stores/user';

export default {
    name: "TravelNews",
    data() {
        return {
            items: [],
            user: null,
            startIndex: 0,
            visibleCount: 3,
            selectedItem: null,
            heading: "TRAVEL NEWS",
            title: "Plan your travel with confidence",
            description:
                "Latest updates and essential travel tips to make your journey stress-free and enjoyable.",
        };
    },
    async created() {
        // fetch news from API
        const userStore = useUserStore();
        this.user = userStore.user;
        this.isAdmin = this.user.role === "admin";

        const response = await apiClient.get("/news/promotions");
        console.log(response.data.data);
        this.items = response.data.data.map((item, index) => ({
            id: item.id,
            number: `0${index + 1}`,
            title: item.title,
            details: item.body,
        }));

    },
    computed: {
        visibleItems() {
            return this.items.slice(this.startIndex, this.startIndex + this.visibleCount);
        },
    },
    methods: {
        scrollUp() {
            if (this.startIndex > 0) this.startIndex--;
        },
        scrollDown() {
            if (this.startIndex < this.items.length - this.visibleCount) this.startIndex++;
        },
        selectItem(item) {
            this.selectedItem = item;
        },
        async handleRemoveNewClick(index) {
            // send request to delete news at DB
            const response = await apiClient.delete(`/news/${this.items[index].id}`);

            if (response.status === 200) {
                this.$toastr.success("News has been removed successfully");
                this.items.splice(index, 1);
                this.selectedItem = null;
            } else {
                this.$toastr.error("Failed to remove news");
            }
        },
    },
};
</script>

<style scoped>
/* Container tổng */
.travel-news-container {
    text-align: center;
    margin: 1.8rem auto;
    max-width: 800px;
}

.travel-heading {
    font-weight: 400;
    font-size: 1rem;
    color: #333;
    letter-spacing: 4px;
    margin-bottom: 0.3rem;
}

.travel-title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.travel-description {
    font-size: 1rem;
    color: #666;
}

.container {
    display: flex;
    justify-content: space-between;
    padding: 2rem;
}

/* Cột trái: danh sách */
.info-list {
    width: 45%;
    max-height: 400px;
    overflow: hidden;
}

.info-card {
    margin-bottom: 0.8rem;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.card-number {
    font-weight: bold;
    color: white;
    background: linear-gradient(135deg, #003D5B, #00577A);
    /* Hiệu ứng gradient */
    border-radius: 50%;
    /* Bo cong để tạo hình oval */
    display: inline-flex;
    /* Hiển thị nội dung linh hoạt */
    justify-content: center;
    /* Căn giữa nội dung theo chiều ngang */
    align-items: center;
    /* Căn giữa nội dung theo chiều dọc */
    width: 30px !important;
    /* Độ rộng của oval */
    height: 20px !important;
    /* Chiều cao của oval */
    text-align: center;
    /* Căn giữa văn bản */
}


.card-title {
    font-size: 1.2rem;
    font-weight: bold;
}

.card-summary {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.2rem;
}

/* Thanh cuốn */
.scrollbar {
    text-align: left;
    margin-top: 0.5rem;
}

.scrollbar button {
    background-color: #00577A;
    color: #fff;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
    margin: 0.2rem;
    border-radius: 4px;
}

/* Cột phải: ảnh cửa sổ máy bay */
.info-details {
    width: 45%;
    position: relative;
}

.image-container {
    position: relative;
    height: 300px;
}

.airplane-window {
    border-radius: 50% / 35%;
    position: absolute;
    transition: all 0.3s ease;
}

.image-small {
    width: 180px;
    height: 280px;
    top: 40px;
    left: 10%;
    z-index: 3;
    /* Ảnh 1 nằm trên */
}

.image-large {
    width: 180px;
    height: 300px;
    top: -30px;
    left: 35%;
    z-index: 2;
    /* Ảnh 2 nằm dưới ảnh 1 */
}

.image-smallest {
    width: 160px;
    height: 260px;
    top: 60px;
    left: 60%;
    z-index: 1;
    /* Ảnh 3 dưới cùng */
}


/* Chi tiết tin tức */
.news-details {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: flex-start;
}

.news-details h2 {
    text-align: start;
    font-size: 1.2rem;
    font-weight: bold;
}

.news-details p {
    text-align: start;

}

.remove-row {
    display: flex;
    flex-direction: row;
    gap: 4px;
}

.remove-icon {
    width: 15px;
    height: 15px;
}

.circle-button {
    /* Đảm bảo khoảng cách giữa nút chính và nút tròn */
    font-size: 30px;
    width: 20px;
    height: 20px;
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
</style>
