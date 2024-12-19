import './assets/main.css'

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
// Import Toastr.js and its CSS
import toastr from 'toastr';
import 'toastr/build/toastr.min.css';


const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);

app.use(pinia);
app.use(router);

// Make toastr globally accessible
app.config.globalProperties.$toastr = toastr;

app.mount("#app");

