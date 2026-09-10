<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <h2>Welcome {{ dashboard.staff_name }}</h2>
                <p class="text-muted">
                    Manage your assigned treks and participants.
                </p>
                <hr>
                <div class="row">
                    <div class="col-md-3">
                        <div class="card text-center shadow">
                            <div class="card-body">
                                <h5>Assigned Treks</h5>
                                <h2>
                                    {{ dashboard.total_assigned_treks }}
                                </h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center shadow">
                            <div class="card-body">
                                <h5>Participants</h5>
                                <h2>
                                    {{ dashboard.total_participants }}
                                </h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center shadow">
                            <div class="card-body">
                                <h5>Open Treks</h5>
                                <h2>
                                    {{ dashboard.open_treks }}
                                </h2>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center shadow">
                            <div class="card-body">
                                <h5>Pending Treks</h5>
                                <h2>
                                    {{ dashboard.pending_treks }}
                                </h2>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Assigned Treks -->
                <h4 class="mt-5 mb-3">
                    Assigned Treks
                </h4>
                <div class="row">
                    <div
                        class="col-lg-4 col-md-6 mb-4"
                        v-for="trek in dashboard.assigned_treks"
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
                                            'bg-secondary': trek.status==='Pending',
                                            'bg-primary': trek.status==='Open',
                                            'bg-success': trek.status==='Active',
                                            'bg-dark': trek.status==='Completed'
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
                                    <strong>Participants:</strong>
                                    {{ trek.participants }}
                                </p>
                                <p>
                                    <strong>Slots:</strong>
                                    {{ trek.available_slots }}
                                </p>
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
    staff_name : "",
    total_assigned_treks: 0,
    total_participants: 0,
    open_treks: 0,
    pending_treks: 0,
    completed_treks: 0,
    assigned_treks: []
});
function formatId(prefix, id) {
    return `${prefix}${String(id).padStart(3,"0")}`;
}
async function loadDashboard() {
    try {
        const response = await api.get("/staff/dashboard");
        dashboard.value = response.data.data;
    }
    catch(err){
        console.error(err);
    }
}
onMounted(loadDashboard);
</script>