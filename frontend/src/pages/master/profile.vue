<template>
    <div class="profile-card">
        <div class="profile-header">
            <img src="@/assets/avatar.jpg" alt="Profile Image" class="profile-image" />
        </div>
        <div class="profile-body">
            <h2 class="profile-name">John Doe</h2>
            <p class="profile-bio">Software Engineer | Tech Enthusiast</p>
            <ul class="profile-info">
                <li>
                    <img src="@/assets/mail.png" alt="Email Icon" class="info-icon" />
                    <span>johndoe@example.com</span>
                </li>
                <li>
                    <img src="@/assets/facebook.png" alt="Facebook Icon" class="info-icon" />
                    <span>facebook.com/johndoe</span>
                </li>
                <li>
                    <img src="@/assets/phone-call.png" alt="Phone Icon" class="info-icon" />
                    <span>+1 234 567 890</span>
                </li>
                <li>
                    <img src="@/assets/address.png" alt="Address Icon" class="info-icon" />
                    <span>123 Main St, City, Country</span>
                </li>
                <li>
                    <img src="@/assets/nation.png" alt="Nation Icon" class="info-icon" />
                    <span>Viet Nam</span>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {};
</script>

<style scoped>
/* Card Container */
.profile-card {
    width: 400px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    background-color: #ffffff;
    margin: 30px auto;
    font-family: Arial, sans-serif;
    max-height: 600px;
}

/* Header Section */
.profile-header {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #00577A, #007A99);
    display: flex;
    justify-content: center;
    align-items: center;
}

.profile-image {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid #ffffff;
    object-fit: cover;
}

/* Body Section */
.profile-body {
    padding: 20px;
    text-align: center;
}

.profile-name {
    font-size: 1.8em;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

.profile-bio {
    font-size: 1em;
    color: #666;
    margin-bottom: 20px;
}

/* Info Section */
.profile-info {
    list-style: none;
    padding: 0;
    margin: 0;
}

.profile-info li {
    display: flex;
    align-items: center;
    justify-content: start;
    font-size: 1em;
    color: #555;
    margin: 10px 0;
}

.info-icon {
    width: 24px;
    height: 24px;
    margin-right: 10px;
}
</style>