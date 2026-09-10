<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <h2>Participants</h2>
                <p class="text-muted">
                    View participants registered for your assigned treks.
                </p>
                <hr>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <label class="form-label">
                            Select Trek
                        </label>
                        <select
                            class="form-select"
                            v-model="selectedTrek"
                            @change="loadParticipants"
                        >
                            <option value="">
                                Select Trek
                            </option>
                            <option
                                v-for="trek in treks"
                                :key="trek.id"
                                :value="trek.id"
                            >
                                {{ trek.name }}
                            </option>
                        </select>
                    </div>
                    <div
                        class="col-md-5"
                        v-if="selectedTrek"
                    >
                        <label class="form-label">
                            Search Participant
                        </label>
                        <input
                            class="form-control"
                            placeholder="Search..."
                            v-model="search"
                        >
                    </div>
                </div>
                <div
                    v-if="selectedTrek"
                    class="mb-3"
                >
                    <strong>
                        Total Participants :
                        {{ participants.length }}
                    </strong>
                </div>
                <div
                    class="table-responsive"
                    v-if="selectedTrek"
                >
                    <table class="table table-bordered table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>User ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Booking Date</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="participant in filteredParticipants"
                                :key="participant.booking_id"
                            >
                                <td>
                                    {{ formatUserId(participant.user.id) }}
                                </td>
                                <td>
                                    {{ participant.user.name }}
                                </td>
                                <td>
                                    {{ participant.user.email }}
                                </td>
                                <td>
                                    {{ participant.user.phone }}
                                </td>
                                <td>
                                    {{ formatDate(participant.booking_date) }}
                                </td>
                                <td>
                                    <button
                                        class="btn btn-outline-primary btn-sm"
                                        @click="openModal(participant)"
                                    >
                                        View
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div
                    v-if="selectedTrek && filteredParticipants.length===0"
                    class="text-center mt-5"
                >
                    <h4>
                        No participants found.
                    </h4>
                </div>
            </div>
        </div>
    </div>
    <!-- Modal -->
    <div
        class="modal fade"
        id="participantModal"
        tabindex="-1"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        Participant Details
                    </h5>
                    <button
                        class="btn-close"
                        @click="closeModal"
                    ></button>
                </div>
                <div
                    class="modal-body"
                    v-if="selectedParticipant"
                >
                    <p>
                        <strong>User ID :</strong>
                        {{ formatUserId(selectedParticipant.user.id) }}
                    </p>
                    <p>
                        <strong>Name :</strong>
                        {{ selectedParticipant.user.name }}
                    </p>
                    <p>
                        <strong>Email :</strong>
                        {{ selectedParticipant.user.email }}
                    </p>
                    <p>
                        <strong>Phone :</strong>
                        {{ selectedParticipant.user.phone }}
                    </p>
                    <p>
                        <strong>Booking ID :</strong>
                        {{ formatBookingId(selectedParticipant.booking_id) }}
                    </p>
                    <p>
                        <strong>Booking Date :</strong>
                        {{ formatDate(selectedParticipant.booking_date) }}
                    </p>
                </div>
                <div class="modal-footer">
                    <button
                        class="btn btn-secondary"
                        @click="closeModal"
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
const treks = ref([]);
const participants = ref([]);
const selectedTrek = ref("");
const search = ref("");
const selectedParticipant = ref(null);
let participantModal = null;
const filteredParticipants = computed(() => {
    if (!search.value)
        return participants.value;
    const keyword = search.value.toLowerCase();
    return participants.value.filter(p =>
        p.user.name.toLowerCase().includes(keyword) ||
        p.user.email.toLowerCase().includes(keyword) ||
        p.user.phone.includes(keyword)
    );
});
async function loadTreks(){
    const response = await api.get("/staff/treks");
    treks.value = response.data.data;
}
async function loadParticipants(){
    if(!selectedTrek.value){
        participants.value = [];
        return;
    }
    const response = await api.get(
        `/staff/treks/${selectedTrek.value}/participants`
    );
    participants.value = response.data.participants;
}
function openModal(participant){
    selectedParticipant.value = participant;
    if(!participantModal){
        participantModal = new Modal(
            document.getElementById("participantModal")
        );
    }
    participantModal.show();
}
function closeModal(){
    participantModal.hide();
    selectedParticipant.value = null;
}
function formatUserId(id){
    return `U${String(id).padStart(3,"0")}`;
}
function formatBookingId(id){
    return `B${String(id).padStart(3,"0")}`;
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
onMounted(loadTreks);
</script>