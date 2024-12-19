<template>
    <div class="admin-post">
        <div class="sidebar">
            <h3 class="post-content">Post Content</h3>
            <ul>
                <li><button @click="selectOption('discount')">Discount Information</button></li>
                <li><button @click="selectOption('news')">News</button></li>
                <li><button @click="selectOption('travel')">Travel Locations</button></li>
            </ul>
        </div>
        <div class="form-container">
            <h2 class="post-content">{{ formTitle }}</h2>
            <form @submit.prevent="handleSubmit">
                <div v-if="selectedOption === 'discount'" class="form-section">
                    <div class="input-row">
                        <div class="input-group">
                            <label for="discount-title">Title:</label>
                            <input type="text" id="discount-title" v-model="formData.title" required />
                        </div>
                        <div class="input-group">
                            <label for="discount-percentage">Discount Percentage:</label>
                            <input type="number" step="0.01" id="discount-percentage"
                                v-model="formData.discountPercentage" required />
                        </div>
                    </div>
                    <div class="input-row">
                        <div class="input-group">
                            <label for="discount-start-date">Start Date:</label>
                            <input type="date" id="discount-start-date" v-model="formData.startDate" required />
                        </div>
                        <div class="input-group">
                            <label for="discount-end-date">End Date:</label>
                            <input type="date" id="discount-end-date" v-model="formData.endDate" required />
                        </div>
                    </div>
                    <div class="input-group">
                        <label for="discount-percentage">Discount Percentage:</label>
                        <input type="number" step="0.01" id="discount-percentage" v-model="formData.discountPercentage"
                            required />
                    </div>
                    <div class="input-group">
                        <label for="discount-image">Image:</label>
                        <input type="file" id="discount-image" @change="handleFileChange" accept=".jpg" required />
                    </div>
                    <div class="input-group">
                        <label for="discount-description">Description:</label>
                        <textarea id="discount-description" v-model="formData.description" required></textarea>
                    </div>
                </div>

                <div v-if="selectedOption === 'news'" class="form-section">
                    <div class="input-group">
                        <label for="news-title">Title:</label>
                        <input type="text" id="news-title" v-model="formData.title" required />
                    </div>
                    <div class="input-group">
                        <label for="news-description">Description:</label>
                        <textarea id="news-description" v-model="formData.description" required></textarea>
                    </div>
                </div>

                <div v-if="selectedOption === 'travel'" class="form-section">
                    <div class="input-row">
                        <div class="input-group">
                            <label for="travel-name">Location Name:</label>
                            <input type="text" id="travel-name" v-model="formData.name" required />
                        </div>
                        <div class="input-group">
                            <label for="travel-image">Image:</label>
                            <input type="file" id="travel-image" @change="handleFileChange" accept=".jpg" required />
                        </div>
                    </div>
                    <div class="input-group">
                        <label for="travel-description">Description:</label>
                        <textarea id="travel-description" v-model="formData.description" required></textarea>
                    </div>
                    <div class="input-group">
                        <label for="travel-link">Website Link:</label>
                        <input type="url" id="travel-link" v-model="formData.link" required />
                    </div>
                </div>

                <button type="submit" class="submit-button">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            selectedOption: '',
            formData: {
                title: '',
                description: '',
                name: '',
                link: '',
                image: null,
            },
        };
    },
    computed: {
        formTitle() {
            switch (this.selectedOption) {
                case 'discount':
                    return 'Post Discount Information';
                case 'news':
                    return 'Post News';
                case 'travel':
                    return 'Post Attractive Travel Locations';
                default:
                    return 'Select an Option';
            }
        },
    },
    methods: {
        selectOption(option) {
            this.selectedOption = option;
            this.resetFormData();
        },
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file && file.type === 'image/jpeg') {
                this.formData.image = file;
            } else {
                alert('Please select a JPG file.');
            }
        },
        handleSubmit() {
            console.log('Form data:', this.formData);
            alert('Data has been submitted. Handle storage on the backend.');
        },
        resetFormData() {
            this.formData = {
                title: '',
                description: '',
                name: '',
                link: '',
                image: null,
            };
        },
    },
};
</script>

<style scoped>
.admin-post {
    display: flex;
    gap: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sidebar {
    flex: 1;
    padding: 10px;
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sidebar h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: #333;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar ul li {
    margin-bottom: 10px;
}

.sidebar ul li button {
    width: 100%;
    padding: 8px;
    background: linear-gradient(135deg, #00577A, #007A99);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: left;
}

.sidebar ul li button:hover {
    background: linear-gradient(135deg, #007A99, #0099B3);
}

.form-container {
    flex: 3;
    padding: 20px;
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.input-row {
    display: flex;
    gap: 20px;
}

.input-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

label {
    font-weight: bold;
    font-size: 14px;
}

input,
textarea {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px 15px;
    background: linear-gradient(135deg, #00577A, #007A99);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: linear-gradient(135deg, #007A99, #0099B3);
}

.submit-button {
    margin-top: 20px;
    align-self: flex-end;
}

.post-content {
    font-weight: bold;
    margin-bottom: 10px;
}
</style>