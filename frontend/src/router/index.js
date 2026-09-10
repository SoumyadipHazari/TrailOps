import { createRouter, createWebHistory } from 'vue-router'

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

import AdminDashboard from "../views/admin/DashboardView.vue";
import AdminTreks from "../views/admin/TrekView.vue";
import AdminStaff from "../views/admin/StaffView.vue";
import AdminUsers from "../views/admin/UserView.vue";
import AdminBookings from "../views/admin/BookingView.vue";

import StaffDashboard from "../views/staff/DashboardView.vue";
import StaffTreks from "../views/staff/TrekView.vue";
import StaffParticipants from "../views/staff/ParticipantsView.vue";

import UserDashboard from "../views/user/DashboardView.vue";
import UserTreks from "../views/user/TrekView.vue";
import UserBookings from "../views/user/BookingView.vue";
import UserProfile from "../views/user/ProfileView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/login"
        },

        {
            path: "/login",
            name: "login",
            component: LoginView
        },

        {
            path: "/register",
            name: "register",
            component: RegisterView
        },

        {
            path: "/admin/dashboard",
            name: "admin-dashboard",
            component: AdminDashboard
        },
        {
            path: "/admin/treks",
            name: "admin-treks",
            component: AdminTreks
        },
        {
            path: "/admin/staff",
            name: "admin-staff",
            component: AdminStaff
        },
        {
            path: "/admin/users",
            name: "admin-users",
            component: AdminUsers
        },
        {
            path: "/admin/bookings",
            name:"admin-bookings",
            component: AdminBookings
        },
        {
            path: "/staff/dashboard",
            name: "staff-dashboard",
            component: StaffDashboard
        },
        {
            path: "/staff/treks",
            name: "staff-trek",
            component: StaffTreks
        },
        {
            path: "/staff/participants",
            name: "staff-participants",
            component: StaffParticipants
        },

        {
            path: "/user/dashboard",
            name: "user-dashboard",
            component: UserDashboard
        },
        {
            path: "/user/treks",
            name: "user-treks",
            component: UserTreks
        },
        {
            path: "/user/bookings",
            name: "user-bookings",
            component: UserBookings
        },
        {
            path: "/user/profile",
            name: "user-profile",
            component: UserProfile
        },

        {
            path: "/:pathMatch(.*)*",
            redirect: "/login"
        }
    ]
});

export default router
