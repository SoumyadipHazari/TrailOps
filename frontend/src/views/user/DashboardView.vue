<template>

    <Navbar />

    <div class="container-fluid">

        <div class="row">

            <div class="col-md-2 p-0">
                <Sidebar />
            </div>

            <div class="col-md-10 p-4">

                <h2>
                    Welcome, {{ dashboard.user_name }}
                </h2>

                <p class="text-muted">
                    Here's an overview of your trekking activities.
                </p>

                <hr>

                <div class="row">

                    <div class="col-md-3 mb-3">

                        <div class="card text-center shadow h-100">

                            <div class="card-body">

                                <h5>Total Bookings</h5>

                                <h2>
                                    {{ dashboard.total_bookings }}
                                </h2>

                            </div>

                        </div>

                    </div>

                    <div class="col-md-3 mb-3">

                        <div class="card text-center shadow h-100">

                            <div class="card-body">

                                <h5>Active Bookings</h5>

                                <h2>
                                    {{ dashboard.active_bookings }}
                                </h2>

                            </div>

                        </div>

                    </div>

                    <div class="col-md-3 mb-3">

                        <div class="card text-center shadow h-100">

                            <div class="card-body">

                                <h5>Completed Treks</h5>

                                <h2>
                                    {{ dashboard.completed_treks }}
                                </h2>

                            </div>

                        </div>

                    </div>

                    <div class="col-md-3 mb-3">

                        <div class="card text-center shadow h-100">

                            <div class="card-body">

                                <h5>Cancelled</h5>

                                <h2>
                                    {{ dashboard.cancelled_bookings }}
                                </h2>

                            </div>

                        </div>

                    </div>

                </div>

                <div class="card shadow mt-4">

                    <div class="card-body">

                        <h4 class="mb-3">
                            Quick Actions
                        </h4>

                        <div class="d-flex flex-wrap gap-3">

                            <button
                                class="btn btn-primary"
                                @click="router.push('/user/treks')"
                            >
                                Browse Treks
                            </button>

                            <button
                                class="btn btn-success"
                                @click="router.push('/user/bookings')"
                            >
                                My Bookings
                            </button>

                            <button
                                class="btn btn-secondary"
                                @click="router.push('/user/profile')"
                            >
                                Profile
                            </button>
                            <button
                                class="btn btn-warning"
                                @click="exportBookingHistory"
                            >
                                Export Booking History
                            </button>

                        </div>

                    </div>

                </div>

                <div class="card shadow mt-4">

                    <div class="card-body">

                        <h4 class="mb-3">
                            Trek History
                        </h4>

                        <div
                            v-if="dashboard.history.length"
                            class="table-responsive"
                        >

                            <table class="table table-hover">

                                <thead>

                                    <tr>

                                        <th>Trek</th>
                                        <th>Location</th>
                                        <th>Difficulty</th>
                                        <th>Completed</th>

                                    </tr>

                                </thead>

                                <tbody>

                                    <tr
                                        v-for="trek in dashboard.history"
                                        :key="trek.trek_name"
                                    >

                                        <td>{{ trek.trek_name }}</td>

                                        <td>{{ trek.location }}</td>

                                        <td>{{ trek.difficulty }}</td>

                                        <td>{{ formatDate(trek.completed_date) }}</td>

                                    </tr>

                                </tbody>

                            </table>

                        </div>

                        <div
                            v-else
                            class="text-muted"
                        >

                            No completed treks yet.

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import api from "../../services/api";

import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";

const router = useRouter();

const dashboard = ref({

    user_name: "",

    total_bookings: 0,

    active_bookings: 0,

    completed_treks: 0,

    cancelled_bookings: 0,
    history: []

});

function formatDate(date) {

    if (!date) return "-";

    return new Date(date).toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );

}

async function exportBookingHistory() {

    try {

        const response = await api.post("/user/export-bookings");

        alert(
            response.data.message +
            "\n\nYour CSV is being generated. It will download automatically once it is ready."
        );

        checkDownloadStatus();

    }

    catch (err) {

        console.error(err);

        alert(
            err.response?.data?.message ||
            "Unable to export booking history."
        );

    }

}

async function checkDownloadStatus() {

    const maxAttempts = 15;

    let attempts = 0;

    const interval = setInterval(async () => {

        attempts++;

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/user/download-bookings",
                {
                    credentials: "include"
                }
            );

            if (response.ok) {

                clearInterval(interval);

                window.open(
                    "http://127.0.0.1:5000/user/download-bookings",
                    "_blank"
                );

                return;

            }

        }

        catch (err) {

            console.log("Waiting for CSV...");

        }

        if (attempts >= maxAttempts) {

            clearInterval(interval);

            alert(
                "CSV generation is taking longer than expected. Please try downloading again in a few moments."
            );

        }

    }, 2000);

}

async function loadDashboard() {

    try {

        const response = await api.get("/user/dashboard");

        dashboard.value = response.data.data;

    }

    catch (err) {

        console.error(err);

        alert(
            err.response?.data?.message ||
            "Unable to load dashboard."
        );

    }

}

onMounted(loadDashboard);

</script>
<style scoped>
    .card{
       transition:0.25s;
    }

    .card:hover{
       transform:translateY(-4px);
    }
</style>