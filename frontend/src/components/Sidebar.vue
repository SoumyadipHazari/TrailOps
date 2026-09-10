<template>

<div class="bg-light border-end vh-100 p-3">

    <h5 class="mb-4">
        {{ panelTitle }}
    </h5>

    <div class="nav flex-column">

        <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            active-class="active-link"
        >
            {{ item.label }}
        </router-link>

    </div>

</div>

</template>

<script setup>

import { computed } from "vue";

import { useRoute } from "vue-router";

const route = useRoute();

const role = computed(() => {
    return route.path.split("/")[1];
});

const panelTitle = computed(() => {

    if (role.value === "admin")
        return "Admin Panel";

    if (role.value === "staff")
        return "Staff Panel";

    return "User Panel";

});

const menuItems = computed(() => {

    if (role.value === "admin") {

        return [

            {
                label: "Dashboard",
                path: "/admin/dashboard"
            },

            {
                label: "Treks",
                path: "/admin/treks"
            },

            {
                label: "Staff",
                path: "/admin/staff"
            },

            {
                label: "Users",
                path: "/admin/users"
            },

            {
                label: "Bookings",
                path: "/admin/bookings"
            }

        ];

    }

    if (role.value === "staff") {

        return [

            {
                label: "Dashboard",
                path: "/staff/dashboard"
            },

            {
                label: "My Treks",
                path: "/staff/treks"
            },

            {
                label: "Participants",
                path: "/staff/participants"
            }

        ];

    }

    if (role.value === "user"){
        return [

            {
                label: "Dashboard",
                path: "/user/dashboard"
            },

            {
                label: "Browse Treks",
                path: "/user/treks"
            },

            {
                label: "My Bookings",
                path: "/user/bookings"
            },

            {
                label: "Profile",
                path: "/user/profile"
            }

        ];
    }

});
</script>
<style scoped>

.nav-link{
    color:black;
    border-radius:8px;
    margin-bottom:8px;
    transition:0.25s;
}

.nav-link:hover{
    background:#e9ecef;
}

.active-link{
    background:#0d6efd;
    color:white !important;
}
</style>