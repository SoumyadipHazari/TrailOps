<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <h2>Bookings</h2>
                <p class="text-muted">
                    View all trek bookings made by users.
                </p>
                <hr>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input
                            class="form-control"
                            placeholder="Search booking..."
                            v-model="search"
                        >
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th>Booking ID</th>
                                <th>User</th>
                                <th>Trek</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="booking in filteredBookings"
                                :key="booking.booking_id"
                            >
                                <td>{{ formatBookingId(booking.booking_id) }}</td>
                                <td>{{ booking.user.name }}</td>
                                <td>{{ booking.trek.name }}</td>
                                <td>{{ formatDate(booking.booking_date) }}</td>
                                <td>
                                    <span
                                        class="badge"
                                        :class="{
                                            'bg-primary': booking.booking_status==='Booked',
                                            'bg-success': booking.booking_status==='Completed',
                                            'bg-danger': booking.booking_status==='Cancelled'
                                        }"
                                    >
                                        {{ booking.booking_status }}
                                    </span>
                                </td>
                                <td>
                                    <button
                                        class="btn btn-outline-primary btn-sm"
                                        @click="openDetailsModal(booking)"
                                    >
                                        View
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div
                    v-if="filteredBookings.length===0"
                    class="text-center mt-5"
                >
                    <h4>No bookings found.</h4>
                </div>
            </div>
        </div>
    </div>
    <div
        class="modal fade"
        id="bookingDetailsModal"
        tabindex="-1"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        Booking Details
                    </h5>
                    <button
                        class="btn-close"
                        @click="closeDetailsModal"
                    ></button>
                </div>
                <div
                    class="modal-body"
                    v-if="selectedBooking"
                >
                    <div class="row">
                        <div class="col-md-6">
                            <h5>User Information</h5>
                            <hr>
                            <p><strong>ID:</strong> {{ formatUserId(selectedBooking.user.id) }}</p>
                            <p><strong>Name:</strong> {{ selectedBooking.user.name }}</p>
                            <p><strong>Email:</strong> {{ selectedBooking.user.email }}</p>
                        </div>
                        <div class="col-md-6">
                            <h5>Trek Information</h5>
                            <hr>
                            <p><strong>ID:</strong> {{ formatTrekId(selectedBooking.trek.id) }}</p>
                            <p><strong>Name:</strong> {{ selectedBooking.trek.name }}</p>
                            <p><strong>Location:</strong> {{ selectedBooking.trek.location }}</p>
                            <p><strong>Status:</strong> {{ selectedBooking.trek.status }}</p>
                        </div>
                    </div>
                    <hr>
                    <p>
                        <strong>Booking Date:</strong>
                        {{ formatDate(selectedBooking.booking_date) }}
                    </p>
                    <p>
                        <strong>Booking Status:</strong>
                        {{ selectedBooking.booking_status }}
                    </p>
                </div>
                <div class="modal-footer">
                    <button
                        class="btn btn-secondary"
                        @click="closeDetailsModal"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import api from "../../services/api";
import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";
const bookings = ref([]);
const search = ref("");
const selectedBooking = ref(null);
let detailsModal = null;
const filteredBookings = computed(() => {
    if (!search.value)
        return bookings.value;

    const keyword = search.value.toLowerCase();
    return bookings.value.filter(b =>
        b.user.name.toLowerCase().includes(keyword) ||
        b.trek.name.toLowerCase().includes(keyword) ||
        formatBookingId(b.booking_id)
            .toLowerCase()
            .includes(keyword)
    );
});

async function loadBookings(){
    try{
        const response = await api.get("/admin/bookings");
        bookings.value = response.data.data;
    }
    catch(err){
        alert(
            err.response?.data?.message ||
            "Unable to load bookings."
        );
    }
}

function openDetailsModal(booking){
    selectedBooking.value = booking;
    if(!detailsModal){
        detailsModal = new Modal(
            document.getElementById("bookingDetailsModal")
        );
    }
    detailsModal.show();
}

function closeDetailsModal(){
    detailsModal.hide();
    selectedBooking.value = null;
}

function formatBookingId(id){
    return `B${String(id).padStart(3,"0")}`;
}

function formatUserId(id){
    return `U${String(id).padStart(3,"0")}`;
}

function formatTrekId(id){
    return `T${String(id).padStart(3,"0")}`;
}

function formatDate(date){
    return new Date(date).toLocaleDateString(
        "en-IN",
        {
            day:"2-digit",
            month:"short",
            year:"numeric"
        }
    );
}

onMounted(loadBookings);

</script>