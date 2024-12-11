<template>
    <footer class="footer w-full bg-[#003D5B] text-white py-8 px-40">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
                <h3 class="font-bold text-lg mb-4">About Qairline</h3>
                <p class="text-sm">Qairline is committed to providing safe, reliable, and exceptional flight
                    experiences.</p>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-4">Useful Links</h3>
                <ul class="text-sm space-y-2">
                    <li><router-link to="/support" class="hover:underline">Customer Support</router-link></li>
                    <li><router-link to="/terms" class="hover:underline">Terms and Conditions</router-link></li>
                    <li><router-link to="/privacy" class="hover:underline">Privacy Policy</router-link></li>
                    <li><router-link to="/careers" class="hover:underline">Careers</router-link></li>
                </ul>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-4">Contact Us</h3>
                <ul class="text-sm space-y-2">
                    <li>Email: <a href="mailto:support@qairline.com" class="hover:underline">support@qairline.com</a>
                    </li>
                    <li>Phone: <a href="tel:+123456789" class="hover:underline">+1 234 567 89</a></li>
                    <li>Address: 123 Airline Avenue, New York, NY</li>
                </ul>
            </div>
        </div>
        <div class="mt-8 border-t border-gray-600 pt-4 text-center text-sm">
            <p>&copy; 2024 Qairline. All rights reserved.</p>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'Footer'
}
</script>

<style scoped>
.footer {
    position: relative;
    width: 100%;
}
</style>