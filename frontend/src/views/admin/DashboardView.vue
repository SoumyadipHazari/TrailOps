<template>

<Navbar />

<div class="container-fluid">
    <div class="row">
        <div class="col-md-2 p-0">
            <Sidebar />
        </div>

        <div class="col-md-10 p-4">
            <h2>Welcome Admin</h2>
            <hr>

            <div class="row">

                <div class="col-md-3">
                    <div class="card text-center shadow">
                        <div class="card-body">
                            <h5>Total Treks</h5>
                            <h2>{{ dashboard.total_treks }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-lg mb-3">
                    <div class="card text-center shadow">
                        <div class="card-body">
                            <h5>Completed Treks</h5>
                            <h2>{{ dashboard.completed_treks }}</h2>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-3">
                    <div class="card text-center shadow">
                        <div class="card-body">
                            <h5>Total Staff</h5>
                            <h2>{{ dashboard.total_staff }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="card text-center shadow">
                        <div class="card-body">
                            <h5>Total Users</h5>
                            <h2>{{ dashboard.total_users }}</h2>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-3">
                    <div class="card text-center shadow">
                        <div class="card-body">
                            <h5>Total Bookings</h5>
                            <h2>{{ dashboard.total_bookings }}</h2>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-md-12">
                    <div class="card shadow">
                        <div class="card-body">
                            <h4 class="mb-3">
                                Quick Actions
                            </h4>

                            <button
                                class="btn btn-warning me-3"
                                @click="sendDailyReminders"
                            >
                                Send Daily Reminders
                            </button>

                            <button
                                class="btn btn-primary"
                                @click="generateMonthlyReport"
                            >
                                Generate Monthly Report
                            </button>
                        </div>
                    </div>
                </div>

            </div>
            <div class="row mt-5">
                <div class="col-md-12">
                    <div class="card shadow">
                        <div class="card-body">
                            <h4 class="mb-3">
                                Global Search
                            </h4>
                            <input
                                type="text"
                                class="form-control"
                                placeholder="Search users, staff or treks..."
                                v-model="searchQuery"
                                @input="searchEverything"
                            >
                        </div>
                    </div>
                </div>
            </div>
            <div
                class="row mt-4"
                v-if="searchQuery.trim()"
            >
                <div class="col-md-4">
                    <div class="card shadow h-100">
                        <div class="card-header bg-success text-white">
                            Treks ({{ searchResults.treks.length }})
                        </div>

                        <ul class="list-group list-group-flush">
                            <li
                                class="list-group-item"
                                v-for="trek in searchResults.treks"
                                :key="trek.id"
                            >
                                <strong>
                                    {{ formatId("T", trek.id) }}
                                </strong>
                                <br>
                                {{ trek.name }}
                                <br>
                                <small class="text-muted">
                                    {{ trek.location }}
                                    •
                                    {{ trek.status }}
                                </small>
                            </li>

                            <li
                                v-if="searchResults.treks.length === 0"
                                class="list-group-item text-muted"
                            >
                                No treks found.
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow h-100">
                        <div class="card-header bg-primary text-white">
                            Staff ({{ searchResults.staff.length }})
                        </div>

                        <ul class="list-group list-group-flush">
                            <li
                                class="list-group-item"
                                v-for="staff in searchResults.staff"
                                :key="staff.id"
                            >
                                <strong>
                                    {{ formatId("S", staff.id) }}
                                </strong>
                                <br>
                                {{ staff.name }}
                                <br>
                                <small class="text-muted">
                                    {{ staff.email }}
                                </small>
                            </li>
                            <li
                                v-if="searchResults.staff.length === 0"
                                class="list-group-item text-muted"
                            >
                                No staff found.
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow h-100">
                        <div class="card-header bg-dark text-white">
                            Users ({{ searchResults.users.length }})
                        </div>

                        <ul class="list-group list-group-flush">
                            <li
                                class="list-group-item"
                                v-for="user in searchResults.users"
                                :key="user.id"
                            >
                                <strong>
                                    {{ formatId("U", user.id) }}
                                </strong>
                                <br>

                                {{ user.name }}

                                <br>

                                <small class="text-muted">
                                    {{ user.email }}
                                </small>

                            </li>

                            <li
                                v-if="searchResults.users.length === 0"
                                class="list-group-item text-muted"
                            >
                                No users found.
                            </li>

                        </ul>

                    </div>

                </div>

            </div>
            <div class="row mt-5">

                <div class="col-md-12">

                    <div class="card shadow">

                        <div class="card-header bg-success text-white">

                            Recently Completed Treks

                        </div>

                        <div class="table-responsive">

                            <table class="table table-hover mb-0">

                                <thead>

                                    <tr>

                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Location</th>
                                        <th>Staff</th>
                                        <th>Participants</th>
                                        <th>Completed On</th>
                                        <th>Action</th>

                                    </tr>

                                </thead>

                                <tbody>

                                    <tr
                                        v-for="trek in trekHistory"
                                        :key="trek.id"
                                    >

                                        <td>

                                            {{ formatId("T", trek.id) }}

                                        </td>

                                        <td>

                                            {{ trek.name }}

                                        </td>

                                        <td>

                                            {{ trek.location }}

                                        </td>

                                        <td>

                                            {{ trek.staff }}

                                        </td>

                                        <td>

                                            {{ trek.participants }}

                                        </td>

                                        <td>

                                            {{ trek.end_date }}

                                        </td>
                                        <td>

                                            <button
                                                class="btn btn-secondary btn-sm"
                                                @click="openHistoryDetails(trek)"
                                            >
                                                View Details
                                            </button>

                                        </td>

                                    </tr>

                                    <tr
                                        v-if="trekHistory.length===0"
                                    >

                                        <td
                                            colspan="7"
                                            class="text-center"
                                        >

                                            No completed treks yet.

                                        </td>

                                    </tr>

                                </tbody>

                            </table>

                        </div>

                    </div>

                </div>

            </div>
            <div
                v-if="showDetailModal"
                class="modal fade show"
                style="display:block;background:rgba(0,0,0,.5)"
            >
                <div class="modal-dialog modal-lg modal-dialog-centered">

                    <div class="modal-content">

                        <div class="modal-header">

                            <h5 class="modal-title">
                                Trek Details
                            </h5>

                            <button
                                class="btn-close"
                                @click="closeDetails"
                            ></button>

                        </div>

                        <div class="modal-body">

                            <div class="card mb-3">

                                <div class="card-header bg-dark text-white">
                                    General Information
                                </div>

                                <div class="card-body">

                                    <div class="row">

                                        <div class="col-md-6">
                                            <strong>Name</strong><br>
                                            {{ selectedTrek.name }}
                                        </div>

                                        <div class="col-md-6">
                                            <strong>Location</strong><br>
                                            {{ selectedTrek.location }}
                                        </div>

                                    </div>

                                    <hr>

                                    <strong>Description</strong>

                                    <p>
                                        {{ selectedTrek.description }}
                                    </p>

                                </div>

                            </div>
                            <div class="card mb-3">

                                <div class="card-header bg-dark text-white">
                                    Trek Details
                                </div>

                                <div class="card-body">

                                    <div class="row">

                                        <div class="col-md-6">

                                            <strong>Difficulty</strong><br>
                                            {{ selectedTrek.difficulty }}

                                        </div>

                                        <div class="col-md-6">

                                            <strong>Duration</strong><br>
                                            {{ selectedTrek.duration }} Days

                                        </div>

                                    </div>

                                    <hr>

                                    <div class="row">

                                        <div class="col-md-6">

                                            <strong>Start Date</strong><br>
                                            {{ formatDate(selectedTrek.start_date) }}

                                        </div>

                                        <div class="col-md-6">

                                            <strong>End Date</strong><br>
                                            {{ formatDate(selectedTrek.end_date) }}

                                        </div>

                                    </div>

                                </div>

                            </div>

                            <div class="card">

                                <div class="card-header bg-dark text-white">
                                    Completion Summary
                                </div>

                                <div class="card-body">

                                    <div class="row">

                                        <div class="col-md-6">

                                            <strong>Status</strong><br>

                                            <span class="badge bg-success">
                                                {{ selectedTrek.status }}
                                            </span>

                                        </div>

                                        <div class="col-md-6">

                                            <strong>Participants</strong><br>
                                            {{ selectedTrek.participants }}

                                        </div>

                                    </div>

                                    <hr>

                                    <strong>Assigned Staff</strong><br>
                                    {{ selectedTrek.staff }}

                                </div>

                            </div>

                        </div>

                        <div class="modal-footer">

                            <button
                                class="btn btn-secondary"
                                @click="closeDetails"
                            >
                                Close
                            </button>

                        </div>

                    </div>

                </div>

            </div>
        </div>
    </div>
</div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../../services/api";
import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";

const dashboard = ref({
    total_treks: 0,
    completed_treks: 0,
    total_staff: 0,
    total_users: 0,
    total_bookings: 0
});

const searchQuery = ref("");
const searchResults = ref({
    users: [],
    staff: [],
    treks: []
});
const trekHistory = ref([]);
const selectedTrek = ref(null);
const showDetailModal = ref(false);
function openHistoryDetails(trek){
    selectedTrek.value = trek;
    showDetailModal.value = true;
}
function closeDetails(){
    showDetailModal.value = false;
    selectedTrek.value = null;
}
function formatId(prefix, id) {
    return `${prefix}${String(id).padStart(3, "0")}`;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}

async function searchEverything() {
    if (searchQuery.value.trim().length < 2) {
        searchResults.value = {
            users: [],
            staff: [],
            treks: []
        };
        return;
    }
    try {
        const response = await api.get(
            `/admin/search?q=${searchQuery.value}`
        );
        searchResults.value = response.data.data;
    }
    catch (err) {
        console.error(err);
    }
}

async function loadHistory(){

    try{

        const response = await api.get(
            "/admin/treks/history"
        );

        trekHistory.value = response.data.data;

    }

    catch(err){

        console.error(err);

    }

}

async function sendDailyReminders() {

    try {

        const response = await api.post(
            "/admin/send-reminders"
        );

        alert(response.data.message);

    }

    catch(err){

        console.error(err);

        alert(
            err.response?.data?.message ||
            "Unable to send reminders."
        );

    }

}

async function generateMonthlyReport() {

    try {

        const response = await api.post(
            "/admin/generate-monthly-report"
        );

        alert(response.data.message);

    }

    catch(err){

        console.error(err);

        alert(
            err.response?.data?.message ||
            "Unable to generate monthly report."
        );

    }

}



async function loadDashboard() {
    const response = await api.get("/admin/dashboard");
    dashboard.value = response.data.data;
}


onMounted(() => {

    loadDashboard();

    loadHistory();

});

</script>

<style scoped>

    .card{
        border-radius:12px;
        transition:0.25s;
    }

    .card:hover{
        transform:translateY(-4px);
    }

</style>