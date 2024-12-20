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
                        <label for="discount-description">Description:</label>
                        <textarea id="discount-description" v-model="formData.description" required></textarea>
                    </div>
                    <div class="input-group">
                        <label for="discount-image">Image:</label>
                        <input type="file" id="discount-image" @change="handleFileChange" accept=".jpg" required />
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
                            <input type="text" id="travel-name" v-model="formData.title" required />
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

import apiClient from '@/api/axios';
import {supabase, supabase_storage_url} from '@/supabase';

import { useUserStore } from '@/stores/user';

export default {
    data() {
        return {
            userId: null,
            selectedOption: '',
            formData: {
                title: '',
                description: '',
                type: null,
                startDate: null,
                endDate: null,
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
                    this.formData.type = 'Discount';
                    return 'Post Discount Information';
                case 'news':
                    this.formData.type = 'Promotion';
                    return 'Post News';
                case 'travel':
                    this.formData.type = 'Destination';
                    return 'Post Attractive Travel Locations';
                default:
                    return 'Select an Option';
            }
        },
    },
    async created() {
        const userStore = useUserStore();
        this.userId = userStore.user.id;
    },
    methods: {
        selectOption(option) {
            this.selectedOption = option;
            this.resetFormData();
        },
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                this.formData.image = file;
            } else {
                this.$toastr.error('Please select an image file.');
            }
        },
        validateDateRange(start_time, end_time) {
            // Parse the input strings into Date objects
            if (!start_time && !end_time) {
                return true;
            }
            const startDate = new Date(start_time);
            const endDate = new Date(end_time);

            // Check if start_time is earlier than end_time
            return startDate < endDate;
        },
        convertDateToISO(dateString) {
            // Parse the input date (YYYY-MM-DD)
            const [year, month, day] = dateString.split('-');

            // Create a new Date object using the parsed values
            const date = new Date(Date.UTC(year, month - 1, day));

            // Convert the Date object to an ISO string
            return date.toISOString();
        },
        isValidWebsiteLink(link) {
            try {
                // Create a URL object; if invalid, it will throw an error
                const url = new URL(link);

                // Check if the protocol is either HTTP or HTTPS
                return url.protocol === "http:" || url.protocol === "https:";
            } catch (error) {
                // If an error is thrown, the URL is invalid
                return false;
            }
        },
        async handleSubmit() {
            console.log('Form data:', this.formData);
            // Handle form submission here

            if (!this.formData.title || !this.formData.description) {
                this.$toastr.error('Please fill in all required fields.');
                return;
            }

            if (!this.validateDateRange(this.formData.startDate, this.formData.endDate)) {
                this.$toastr.error('Invalid date range. Please try again.');
                return;
            }

            try {
                if (this.formData.image) {
                    console.log('Image:', this.formData.image.name);
                    const { data, error } = await supabase.storage.from('QAirline-assets').upload(`${this.formData.image.name}`, this.formData.image);
                    console.log(data)
                    if(error) {
                        console.error(error);
                        this.$toastr.error('Failed to upload image. Please try again.');
                        return;
                    }

                    this.formData.imageUrl = `${supabase_storage_url}/${this.formData.image.name}`;
                }
                

                let response = null;
                if (this.formData.type === 'Discount') {
                    response = await this.handleSubmitDiscount();
                } else if (this.formData.type === 'Promotion' || this.formData.type === 'Destination') {
                    if (this.formData.type === 'Destination' && !this.isValidWebsiteLink(this.formData.link)) {
                        this.$toastr.error('Invalid website link. Please try again.');
                        return;
                    }
                    response = await this.handleSubmitNews();
                } else {
                    this.$toastr.error('Invalid form data. Please try again.');
                    return
                }

                if (response.status === 200) {
                    this.$toastr.success('Data has been saved successfully.');
                } else {
                    this.$toastr.error('Failed to post Data. Please try again.');
                }

            } catch(error) {
                console.error(error);
                this.$toastr.error('Failed to upload data. Please try again.');
                return;
            }

            this.resetFormData();
        },
        async handleSubmitDiscount() {
            // validate the date
            const payload = {
                name: this.formData.title,
                description: this.formData.description,
                discount_factor: this.formData.discountPercentage,
                start_time: this.formData.startDate,
                end_time: this.formData.endDate,
                image_url: this.formData.imageUrl,
            };

            const response = await apiClient.post('/discounts', payload);

            return response;

        },
        async handleSubmitNews() {
            const payload = {
                author_id: this.userId,
                title: this.formData.title,
                body: this.formData.description,
                category: this.formData.type,
                image_url: this.formData.imageUrl,
                external_article_link: this.formData.link,
            };

            const response = await apiClient.post('/news', payload);

            return response;
        },
        resetFormData() {
            this.formData = {
                title: '',
                type: null,
                description: '',
                startDate: null,
                endDate: null,
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