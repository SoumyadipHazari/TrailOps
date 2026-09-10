<template>

    <Navbar />

    <div class="container-fluid">

        <div class="row">

            <div class="col-md-2 p-0">
                <Sidebar />
            </div>

            <div class="col-md-10 p-4">

                <h2>My Bookings</h2>

                <p class="text-muted">
                    View and manage your trek bookings.
                </p>

                <hr>

                <div class="row">

                    <div
                        class="col-lg-6 mb-4"
                        v-for="booking in bookings"
                        :key="booking.booking_id"
                    >

                        <div class="card shadow h-100">

                            <div class="card-body">

                                <div class="d-flex justify-content-between">

                                    <h5>

                                        {{ booking.trek.name }}

                                    </h5>

                                    <span
                                        class="badge"
                                        :class="{
                                            'bg-primary': booking.booking_status === 'Booked',
                                            'bg-success': booking.booking_status === 'Completed',
                                            'bg-danger': booking.booking_status === 'Cancelled'
                                        }"
                                    >

                                        {{ booking.booking_status }}

                                    </span>

                                </div>

                                <p class="text-muted">

                                    {{ formatBookingId(booking.booking_id) }}

                                </p>

                                <p>

                                    <strong>Location:</strong>

                                    {{ booking.trek.location }}

                                </p>

                                <p>

                                    <strong>Difficulty:</strong>

                                    {{ booking.trek.difficulty }}

                                </p>

                                <p>

                                    <strong>Duration:</strong>

                                    {{ booking.trek.duration }} Days

                                </p>

                                <p>

                                    <strong>Booking Date:</strong>

                                    {{ formatDate(booking.booking_date) }}

                                </p>

                                <p>

                                    <strong>Trek Status:</strong>

                                    {{ booking.trek.status }}

                                </p>

                            </div>

                            <div class="card-footer bg-white">

                                <button
                                    class="btn btn-outline-primary btn-sm me-2"
                                    @click="openDetailsModal(booking)"
                                >

                                    View Details

                                </button>

                                <button
                                    class="btn btn-danger btn-sm"
                                    @click="cancelBooking(booking.booking_id)"
                                    :disabled="booking.booking_status !== 'Booked' ||
                                        ['Active','Completed'].includes(booking.trek.status)"

                                >

                                    {{
                                        booking.booking_status === "Booked"
                                            ? "Cancel Booking"
                                            : booking.booking_status
                                    }}

                                </button>

                            </div>

                        </div>

                    </div>

                    <div
                        v-if="bookings.length === 0"
                        class="col-12 text-center mt-5"
                    >

                        <h4>No bookings yet</h4>

                        <p class="text-muted">

                            Book your first trek to begin your adventure.

                        </p>

                        <button
                            class="btn btn-primary"
                            @click="router.push('/user/treks')"
                        >

                            Browse Treks

                        </button>

                    </div>

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

                        {{ selectedBooking?.trek.name }}

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

                            <p>

                                <strong>Booking ID:</strong>

                                {{ formatBookingId(selectedBooking.booking_id) }}

                            </p>

                            <p>

                                <strong>Booking Date:</strong>

                                {{ formatDate(selectedBooking.booking_date) }}

                            </p>

                            <p>

                                <strong>Status:</strong>

                                {{ selectedBooking.booking_status }}

                            </p>

                            <p>

                                <strong>Location:</strong>

                                {{ selectedBooking.trek.location }}

                            </p>

                            <p>

                                <strong>Difficulty:</strong>

                                {{ selectedBooking.trek.difficulty }}

                            </p>

                        </div>

                        <div class="col-md-6">

                            <p>

                                <strong>Duration:</strong>

                                {{ selectedBooking.trek.duration }} Days

                            </p>

                            <p>

                                <strong>Start Date:</strong>

                                {{ formatDate(selectedBooking.trek.start_date) }}

                            </p>

                            <p>

                                <strong>End Date:</strong>

                                {{ formatDate(selectedBooking.trek.end_date) }}

                            </p>

                            <p>

                                <strong>Trek Status:</strong>

                                {{ selectedBooking.trek.status }}

                            </p>

                        </div>

                    </div>

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

import { ref, onMounted } from "vue";

import { useRouter } from "vue-router";

import { Modal } from "bootstrap";

import api from "../../services/api";

import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";

const router = useRouter();

const bookings = ref([]);

const selectedBooking = ref(null);

let detailsModal = null;

async function loadBookings() {

    try {

        const response = await api.get("/user/bookings");

        bookings.value = response.data.data;

    }

    catch (err) {

        console.error(err);

    }

}

function formatBookingId(id) {

    return `B${String(id).padStart(3, "0")}`;

}
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

async function cancelBooking(id) {

    if (!confirm("Cancel this booking?")) return;

    try {

        await api.put(
            `/user/bookings/${id}/cancel`
        );

        alert("Booking cancelled.");

        await loadBookings();

    }

    catch (err) {

        alert(
            err.response?.data?.message ||
            "Unable to cancel booking."
        );

    }

}

function openDetailsModal(booking) {

    selectedBooking.value = booking;

    if (!detailsModal) {

        detailsModal = new Modal(
            document.getElementById("bookingDetailsModal")
        );

    }

    detailsModal.show();

}

function closeDetailsModal() {

    if (detailsModal) {

        detailsModal.hide();

    }

    selectedBooking.value = null;

}

onMounted(loadBookings);

</script>