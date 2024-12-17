import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from '@/stores/user';

import dashboard from '../pages/master/dashboard.vue';
import booking from '../pages/master/booking.vue';
import myFlight from "@/pages/master/myflight.vue";
import flightSchedule from "@/pages/master/flightSchedule.vue";
import login from "@/pages/auth/login.vue";
import register from "@/pages/auth/register.vue";

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
                component: myFlight,
                meta: { requiresAuth: true }
            },
            {
                name: 'flightSchedule',
                path: '/flightSchedule',
                component: flightSchedule,
                meta: { requiresAuth: true }
            },
            {
                name: 'Login',
                path: '/login',
                component: login,
            },
            {
                name: 'Register',
                path: '/register',
                component: register,
            }
        ]
    },
];

const router = new createRouter({
    history: createWebHistory(),
    routes,
});


// Global Navigation Guard
router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    if (to.meta.requiresAuth && !userStore.isLoggedIn) {
        // Redirect to login page if not authenticated
        next({ name: 'Login' });
    } else {
        next(); // Proceed to the route
    }
});


export default router;