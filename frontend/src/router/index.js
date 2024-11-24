import { createRouter, createWebHistory } from "vue-router";

import dashboard from '../pages/master/dashboard.vue';
import booking from '../pages/master/booking.vue';
import myFlight from "@/pages/master/myflight.vue";
import flightSchedule from "@/pages/master/flightSchedule.vue";


const routes = [
    {
        name: 'Dashboard',
        path: '/',
        component: dashboard,
        redirect: '/booking',
        children: [
            {
                name: 'booking',
                path: '/booking',
                component: booking
            },
            {
                name: 'myFlight',
                path: '/myflight',
                component: myFlight
            },
            {
                name: 'flightSchedule',
                path: '/flightSchedule',
                component: flightSchedule
            }
        ]
    },

];

const router = Router();
export default router;
function Router() {
    const router = new createRouter({
        history: createWebHistory(),
        routes,
    });
    return router;
}