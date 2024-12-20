<template>
    <div class="history-container">
        <div class="header" @click="toggleDropdown">
            <div class="arrow" :class="{ 'arrow-down': isOpen }"></div>
            <span class="title">Lịch sử thao tác</span>
        </div>
        <div class="dropdown" v-if="isOpen">
            <div v-for="(action, index) in actions" :key="index" class="action-item">
                <div class="action-row">
                    <h3 class="action-title">{{ action.title }}</h3>
                    <p class="action-description">{{ action.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import apiClient from '@/api/axios';

export default {
    data() {
        return {
            isOpen: false,
            userId: null,
            actions: [],
        };
    },
    async created() {
        const userStore = useUserStore();
        this.userId = userStore.user.id;

        try {
            const response = await apiClient.get(`/notifications/${userStore.user.id}`);

            this.actions = response.data.data.map((noti) => ({
                id: noti.notification_id,
                title: noti.notifications.title,
                is_read: noti.is_read,
                description: noti.notifications.description,
            }));
            console.log(this.actions);
        } catch (error) {
            console.error(error);
            this.$toastr.error('Failed to fetch notifications');
        }
    },
    methods: {
        toggleDropdown() {
            this.isOpen = !this.isOpen;
        },
    },
};
</script>

<style scoped>
.history-container {
    font-family: Arial, sans-serif;
    width: 100%;
    max-width: 400px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 10px;
    background: linear-gradient(135deg, #00577A, #007A99);
    color: white;
    cursor: pointer;
    border-top-right-radius: 15px;
    border-top-left-radius: 15px;
}

.arrow {
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid white;
    margin-right: 8px;
    transition: transform 0.3s;
}

.arrow-down {
    transform: rotate(180deg);
}

.title {
    font-size: 16px;
    font-weight: bold;
}

.dropdown {
    background-color: white;
    padding: 10px;
    border: 1px solid #ddd;
    border-top: none;
    border-bottom-right-radius: 15px;
    border-bottom-left-radius: 15px;
}

.action-item {
    margin-bottom: 10px;
}

.action-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #ddd;
    padding: 5px 0;
}

.action-title {
    font-size: 14px;
    font-weight: bold;
    margin: 0;
    flex: 1;
    color: #333;
}

.action-description {
    font-size: 12px;
    margin: 0;
    flex: 2;
    color: #555;
    text-align: right;
    padding-left: 10px;
}
</style>
