<template>
    <div class="loading-container">
        <div class="spinner"></div>
    </div>
</template>

<script>
export default {
    name: "LoadingSpinner",
};
</script>

<style scoped>
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* Chiều cao toàn màn hình */
    background-color: #f8f9fa;
    /* Màu nền tùy chọn */
}

.spinner {
    width: 80px;
    height: 80px;
    border: 8px solid rgba(0, 61, 91, 0.3);
    /* Màu xám nhạt */
    border-top: 8px solid transparent;
    border-left: 8px solid transparent;
    border-right: 8px solid linear-gradient(135deg, #003D5B, #00577A);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>