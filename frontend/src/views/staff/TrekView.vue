<template>

    <Navbar />

    <div class="container-fluid">

        <div class="row">

            <div class="col-md-2 p-0">
                <Sidebar />
            </div>

            <div class="col-md-10 p-4">

                <h2>My Treks</h2>

                <p class="text-muted">
                    Manage your assigned treks.
                </p>

                <div class="row mb-4">

                    <div class="col-md-5">

                        <input
                            class="form-control"
                            placeholder="Search treks..."
                            v-model="search"
                        >

                    </div>

                </div>

                <hr>

                <div class="row">

                    <div
                        class="col-lg-6 mb-4"
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
                                            'bg-secondary': trek.status === 'Pending',
                                            'bg-primary': trek.status === 'Open',
                                            'bg-success': trek.status === 'Active',
                                            'bg-dark': trek.status === 'Completed'
                                        }"
                                    >
                                        {{ trek.status }}
                                    </span>

                                </div>

                                <p class="text-muted">
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
                                    <strong>Participants:</strong>
                                    {{ trek.participants }}
                                </p>
                                <p>
                                    <strong>Start Date:</strong>
                                    {{ formatDate(trek.start_date) }}
                                </p>

                                <p>
                                    <strong>End Date:</strong>
                                    {{ formatDate(trek.end_date) }}
                                </p>

                                <div class="mb-3">

                                    <label class="form-label">
                                        Available Slots
                                    </label>

                                    <input
                                        type="number"
                                        min="0"
                                        class="form-control"
                                        v-model.number="trek.available_slots"
                                        :disabled="['Active','Completed'].includes(trek.status)"
                                    >

                                </div>

                                <div class="mb-3">

                                    <label class="form-label">
                                        Trek Status
                                    </label>

                                    <select
                                        class="form-select"
                                        v-model="trek.status"
                                        :disabled="trek.status === 'Completed'"
                                    >

                                        <option
                                            v-for="status in nextStatuses(trek.status)"
                                            :key="status"
                                            :value="status"
                                        >
                                            {{ status }}
                                        </option>

                                    </select>

                                </div>

                            </div>

                            <div class="card-footer bg-white">

                                <button
                                    class="btn btn-success btn-sm me-2"
                                    @click="updateSlots(trek)"
                                    :disabled="['Active','Completed'].includes(trek.status)"
                                >
                                    Save Slots
                                </button>

                                <button
                                    class="btn btn-primary btn-sm me-2"
                                    @click="updateStatus(trek)"
                                >
                                    Update Status
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

import { ref, computed, onMounted } from "vue";

import api from "../../services/api";

import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";

const treks = ref([]);
const search = ref("");
const loading = ref(false);
const filteredTreks = computed(() => {

    if (!search.value)
        return treks.value;

    const keyword = search.value.toLowerCase();

    return treks.value.filter(trek =>

        trek.name.toLowerCase().includes(keyword) ||

        trek.location.toLowerCase().includes(keyword) ||

        trek.difficulty.toLowerCase().includes(keyword) ||

        trek.status.toLowerCase().includes(keyword) ||

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

function nextStatuses(status) {

    if (status === "Pending")
        return ["Open"];

    if (status === "Open")
        return ["Active"];

    if (status === "Active")
        return ["Completed"];

    return ["Completed"];

}

async function loadTreks() {

    try {

        const response = await api.get("/staff/treks");

        treks.value = response.data.data;

    }

    catch(err){

        console.error(err);

    }

}

async function updateSlots(trek){

    try{

        await api.put(

            `/staff/treks/${trek.id}/slots`,

            {
                available_slots: trek.available_slots
            }

        );

        alert("Slots updated successfully.");

        await loadTreks();

    }

    catch(err){

        alert(
            err.response?.data?.message ||
            "Unable to update slots."
        );

    }

}

async function updateStatus(trek){

    try{

        if(loading.value) return;
        loading.value = true;
        await api.put(

            `/staff/treks/${trek.id}/status`,

            {
                status: trek.status
            }

        );

        alert("Status updated successfully.");

        await loadTreks();

    }
    catch(err){

        alert(
            err.response?.data?.message ||
            "Unable to update status."
        );

    }
    finally{
        loading.value = false;
    }

}

onMounted(loadTreks);

</script>