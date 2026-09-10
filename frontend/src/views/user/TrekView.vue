<template>

    <Navbar />

    <div class="container-fluid">

        <div class="row">

            <div class="col-md-2 p-0">
                <Sidebar />
            </div>

            <div class="col-md-10 p-4">

                <h2>Browse Treks</h2>

                <p class="text-muted">
                    Browse and book available trekking adventures.
                </p>
                <div class="row mb-4">

                    <div class="col-md-5">

                        <input
                            class="form-control"
                            placeholder="Search by trek, location, guide, difficulty, status or ID..."
                            v-model="search"
                        >

                    </div>

                </div>

                <hr>

                <div class="row">

                    <div
                        class="col-lg-4 col-md-6 mb-4"
                        v-for="trek in filteredTreks"
                        :key="trek.id"
                    >

                        <div class="card shadow h-100">

                            <div class="card-body">

                                <div class="d-flex justify-content-between">

                                    <h5>
                                        {{ trek.name }}
                                    </h5>

                                    <span
                                        class="badge"
                                        :class="{
                                            'bg-primary': trek.status === 'Open',
                                            'bg-success': trek.status === 'Active'
                                        }"
                                    >
                                        {{ trek.status }}
                                    </span>

                                </div>

                                <p class="text-muted mb-2">
                                    {{ formatId("T", trek.id) }}
                                </p>

                                <p>
                                    <strong>Location:</strong>
                                    {{ trek.location }}
                                </p>

                                <p>
                                    <strong>Difficulty:</strong>
                                    {{ trek.difficulty }}
                                </p>

                                <p>
                                    <strong>Duration:</strong>
                                    {{ trek.duration }} Days
                                </p>

                                <p>
                                    <strong>Slots:</strong>
                                    {{ trek.available_slots }}
                                </p>

                                <p>
                                    <strong>Guide:</strong>
                                    {{ trek.staff || "Not Assigned" }}
                                </p>

                            </div>

                            <div class="card-footer bg-white">

                                <button
                                    class="btn btn-outline-primary btn-sm me-2"
                                    @click="openDetailsModal(trek)"
                                >
                                    View Details
                                </button>

                                <button
                                    class="btn btn-success btn-sm"
                                    :disabled="
                                    trek.status !== 'Open' ||
                                    trek.available_slots === 0 ||
                                    trek.already_booked
                                    "
                                    @click="bookTrek(trek.id)"
                                >
                                    {{
                                        trek.already_booked
                                            ? "Booked"
                                            : trek.available_slots === 0
                                                ? "Full"
                                                : trek.status === "Open"
                                                    ? "Book Trek"
                                                    : "Trek Ongoing"
                                    }}
                                </button>

                            </div>

                        </div>

                    </div>

                    <div
                        v-if="filteredTreks.length === 0"
                        class="col-12 text-center mt-5"
                    >

                        <h4>No treks available</h4>

                        <p class="text-muted">
                            Please check again later.
                        </p>

                    </div>

                </div>
                <div
                    class="modal fade"
                    id="trekDetailsModal"
                    tabindex="-1"
                >

                    <div class="modal-dialog modal-lg">

                        <div class="modal-content">

                            <div class="modal-header">

                                <h5 class="modal-title">

                                    {{ selectedTrek?.name }}

                                </h5>

                                <button
                                    class="btn-close"
                                    @click="closeDetailsModal"
                                ></button>

                            </div>

                            <div class="modal-body" v-if="selectedTrek">

                                <div class="row">

                                    <div class="col-md-6">

                                        <p>
                                            <strong>Location:</strong>
                                            {{ selectedTrek.location }}
                                        </p>

                                        <p>
                                            <strong>Difficulty:</strong>
                                            {{ selectedTrek.difficulty }}
                                        </p>

                                        <p>
                                            <strong>Duration:</strong>
                                            {{ selectedTrek.duration }} Days
                                        </p>

                                        <p>
                                            <strong>Guide:</strong>
                                            {{ selectedTrek.staff || "Not Assigned" }}
                                        </p>

                                    </div>

                                    <div class="col-md-6">

                                        <p>
                                            <strong>Status:</strong>
                                            {{ selectedTrek.status }}
                                        </p>

                                        <p>
                                            <strong>Available Slots:</strong>
                                            {{ selectedTrek.available_slots }}
                                        </p>

                                        <p>
                                            <strong>Start Date:</strong>
                                            {{ formatDate(selectedTrek.start_date) }}
                                        </p>

                                        <p>
                                            <strong>End Date:</strong>
                                            {{ formatDate(selectedTrek.end_date) }}
                                        </p>

                                    </div>

                                </div>

                                <hr>

                                <h6>Description</h6>

                                <p>

                                    {{ selectedTrek.description || "No description available." }}

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

            </div>

        </div>

    </div>

</template>

<script setup>
import { Modal } from "bootstrap";
import { ref, computed, onMounted } from "vue";

import api from "../../services/api";

import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";

const treks = ref([]);
const selectedTrek = ref(null);
const search = ref("");

let detailsModal = null;
const filteredTreks = computed(() => {

    if (!search.value.trim()) {

        return treks.value;

    }

    const keyword = search.value.toLowerCase();

    return treks.value.filter(trek =>

        trek.name.toLowerCase().includes(keyword) ||

        trek.location.toLowerCase().includes(keyword) ||

        trek.difficulty.toLowerCase().includes(keyword) ||

        trek.status.toLowerCase().includes(keyword) ||

        (trek.staff || "")
            .toLowerCase()
            .includes(keyword) ||

        formatId("T", trek.id)
            .toLowerCase()
            .includes(keyword)

    );

});
function formatId(prefix, id) {

    return `${prefix}${String(id).padStart(3, "0")}`;

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

function openDetailsModal(trek) {

    selectedTrek.value = trek;

    if (!detailsModal) {

        detailsModal = new Modal(
            document.getElementById("trekDetailsModal")
        );

    }

    detailsModal.show();

}
function closeDetailsModal() {

    if (detailsModal) {

        detailsModal.hide();

    }

    selectedTrek.value = null;

}
async function loadTreks() {

    try {

        const response = await api.get("/user/treks");
        console.log(response.data);
        console.log(treks.value);

        treks.value = response.data.data;

    }

    catch (err) {

        console.error(err);

    }

}

async function bookTrek(trekId) {

    if (!confirm("Book this trek?")) return;

    try {

        await api.post("/user/bookings", {
            trek_id: trekId
        });

        alert("Trek booked successfully.");

        await loadTreks();

    }

    catch (err) {

        alert(
            err.response?.data?.message ||
            "Booking failed."
        );

    }

}

onMounted(loadTreks);

</script>

<style scoped>

    .card{
        transition:.25s;
    }

    .card:hover{
        transform:translateY(-4px);
    }

</style>