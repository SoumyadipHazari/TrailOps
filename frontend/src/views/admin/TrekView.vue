<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <div class="row align-items-center mb-4">
                    <div class="col-md-4">
                        <h2 class="mb-0">
                            Trek Management
                        </h2>
                    </div>
                    <div class="col-md-5">
                        <input
                            class="form-control"
                            type="text"
                            placeholder="Search by ID, name, location, staff..."
                            v-model="search"
                        >
                    </div>
                    <div class="col-md-3 text-end">
                        <button
                            class="btn btn-success"
                            @click="openModal"
                        >
                            Add Trek
                        </button>
                    </div>
                </div>
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Location</th>
                            <th>Difficulty</th>
                            <th>Duration</th>
                            <th>Status</th>
                            <th>Assigned Staff</th>
                            <th>Slots</th>
                            <th>Bookings</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="trek in filteredTreks"
                            :key="trek.id"
                        >
                            <td>{{ formatId("T", trek.id) }}</td>
                            <td>{{ trek.name }}</td>
                            <td>{{ trek.location }}</td>
                            <td>{{ trek.difficulty }}</td>
                            <td>{{ trek.duration }} Days</td>
                            <td>
                                <span
                                    class = "badge"
                                    :class="{
                                        'bg-warning': trek.status === 'Pending',
                                        'bg-primary': trek.status === 'Open',
                                        'bg-success': trek.status === 'Active',
                                        'bg-danger': trek.status === 'Completed',
                                        'bg-secondary': trek.status === 'Inactive'
                                    }"
                                >
                                {{ trek.status }}
                                </span>
                            </td>
                            <td>
                                <span v-if="trek.staff_id">
                                    {{ formatId("S", trek.staff_id) }}
                                    -
                                    {{ trek.staff_name }}
                                </span>
                                <span
                                    v-else
                                    class="text-muted"
                                >
                                    Not Assigned
                                </span>
                            </td>
                            <td>{{ trek.available_slots }}</td>
                            <td>{{ trek.booking_count }}</td>
                            <td>
                                <button
                                    class="btn btn-primary btn-sm me-2"
                                    :disabled="trek.status !== 'Pending'"
                                    @click="editTrek(trek)"
                                >
                                    Edit
                                </button>
                                <button
                                    class = "btn btn-info btn-sm me-2"
                                    :disabled="trek.status !== 'Pending'"
                                    @click="openAssignModal(trek)"
                                >
                                    Assign Staff
                                </button>
                                <button
                                    class="btn btn-secondary btn-sm me-2"
                                    @click="openDetailsModal(trek)"
                                >
                                    View
                                </button>
                                <button
                                    class="btn btn-sm"
                                    :class="trek.status === 'Inactive'
                                        ? 'btn-success'
                                        : 'btn-danger'"
                                    :disabled="['Open', 'Active', 'Completed'].includes(trek.status)"
                                    @click="toggleStatus(trek)"
                                >
                                    {{ trek.status === "Inactive" ? "Activate" : "Deactivate" }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                    <tr v-if="filteredTreks.length === 0">
                        <td colspan="10" class="text-center">
                            No treks found.
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div
        class="modal fade"
        id="addTrekModal"
        tabindex="-1"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        {{ isEditing ? "Edit Trek" : "Add Trek" }}
                    </h5>
                    <button
                        class="btn-close"
                        data-bs-dismiss="modal"
                    >
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label>Name</label>
                            <input
                                class="form-control"
                                v-model="trekForm.name"
                            >
                        </div>
                        <div class="col-md-6 mb-3">
                            <label>Location</label>
                            <input
                                class="form-control"
                                v-model="trekForm.location"
                            >
                        </div>
                        <div class="col-md-12 mb-3">
                            <label>Description</label>
                            <textarea
                                class="form-control"
                                rows="3"
                                v-model="trekForm.description"
                            ></textarea>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label>Difficulty</label>
                            <select
                                class="form-select"
                                v-model="trekForm.difficulty"
                            >
                                <option>Easy</option>
                                <option>Moderate</option>
                                <option>Hard</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                Trek Duration(Days)
                            </label>
                            <input
                                type="number"
                                class="form-control"
                                v-model.number="trekForm.duration"
                                min = "1"
                                step = "1"
                                required
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Start Date</label>
                            <input
                                type="date"
                                class="form-control"
                                v-model="trekForm.start_date"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>End Date</label>
                            <input
                                type="date"
                                class="form-control"
                                v-model="trekForm.end_date"
                            >
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button
                        class="btn btn-secondary"
                        @click="closeModal"
                    >
                        Cancel
                    </button>
                    <button
                        class="btn btn-success"
                        @click="saveTrek"
                    >
                        Save Trek
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div
        class="modal fade"
        id="assignStaffModal"
        tabindex="-1"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        Assign Staff
                    </h5>
                    <button
                        class="btn-close"
                        data-bs-dismiss="modal"
                    ></button>
                </div>
                <div class="modal-body">
                    <label class="form-label">
                        Select Staff
                    </label>
                    <select
                        class="form-select"
                        v-model="selectedStaff"
                    >
                        <option value="">
                            -- Not Assigned --
                        </option>
                        <option
                            v-for="staff in activeStaff"
                            :key="staff.id"
                            :value="staff.id"
                        >
                            {{ formatId("S", staff.id) }} - {{ staff.name }}
                        </option>
                    </select>
                </div>
                <div class="modal-footer">
                    <button
                        class="btn btn-secondary"
                        @click="closeAssignModal"
                    >
                        Cancel
                    </button>
                    <button
                        class="btn btn-success"
                        @click="assignStaff"
                    >
                        Assign
                    </button>
                </div>
            </div>
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
                        Trek Details
                    </h5>
                    <button
                        class="btn-close"
                        data-bs-dismiss="modal"
                    ></button>
                </div>
                <div
                    class="modal-body"
                    v-if="viewTrek"
                >
                    <div class="card mb-3">
                        <div class="card-header bg-dark text-white">
                            General Information
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <strong>Name</strong>
                                <p class="mb-0">
                                    {{ viewTrek.name }}
                                </p>
                            </div>
                            <div class="mb-3">
                                <strong>Location</strong>
                                <p class="mb-0">
                                    {{ viewTrek.location }}
                                </p>
                            </div>
                            <div>
                                <strong>Description</strong>
                                <p class="mb-0">
                                    {{ viewTrek.description }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="card mb-3">
                        <div class="card-header bg-dark text-white">
                            Trek Information
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <strong>Difficulty</strong>
                                    <p>{{ viewTrek.difficulty }}</p>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <strong>Duration</strong>
                                    <p>{{ viewTrek.duration }} Days</p>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <strong>Start Date</strong>
                                    <p>
                                        {{ formatDate(viewTrek.start_date) }}
                                    </p>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <strong>End Date</strong>
                                    <p>
                                        {{ formatDate(viewTrek.end_date) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header bg-dark text-white">
                            Management
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <strong>Status</strong>
                                    <br>
                                    <span
                                        class="badge"
                                        :class="{
                                            'bg-warning': viewTrek.status === 'Pending',
                                            'bg-primary': viewTrek.status === 'Open',
                                            'bg-success': viewTrek.status === 'Active',
                                            'bg-danger': viewTrek.status === 'Completed',
                                            'bg-secondary': viewTrek.status === 'Inactive'
                                        }"
                                    >
                                        {{ viewTrek.status }}
                                    </span>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <strong>Available Slots</strong>
                                    <p>
                                        {{ viewTrek.available_slots }}
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <strong>Current Bookings</strong>
                                    <p>
                                        {{ viewTrek.booking_count }}
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <strong>Assigned Staff</strong>
                                    <p>
                                        <span v-if="viewTrek.staff_id">
                                            {{ formatId("S", viewTrek.staff_id) }}
                                            -
                                            {{ viewTrek.staff_name }}
                                        </span>
                                        <span
                                            v-else
                                            class="text-muted"
                                        >
                                            Not Assigned
                                        </span>
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <strong>Created On</strong>
                                    <p>
                                        {{ formatDate(viewTrek.created_at) }}
                                    </p>
                                </div>
                            </div>
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
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import api from "../../services/api";
import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";
const treks = ref([]);
const search = ref("");
const initialForm = {
    name: "",
    location: "",
    description: "",
    difficulty: "Easy",
    duration: 1,
    start_date: "",
    end_date: "",
};
const filteredTreks = computed(() => {
    if (!search.value.trim()) {
        return treks.value;
    }
    const keyword = search.value.toLowerCase().trim();
    return treks.value.filter(trek =>
        formatId("T", trek.id).toLowerCase().includes(keyword) ||
        trek.name.toLowerCase().includes(keyword) ||
        trek.location.toLowerCase().includes(keyword) ||
        trek.difficulty.toLowerCase().includes(keyword) ||
        trek.status.toLowerCase().includes(keyword) ||
        (trek.staff_name || "").toLowerCase().includes(keyword)
    );
});
const activeStaff = ref([]);
const selectedStaff = ref("");
const selectedTrek = ref(null);
const viewTrek = ref(null);
let detailsModal = null;
const trekForm = ref({ ...initialForm });
const isEditing = ref(false);
const editingId = ref(null);
let assignModal = null;
let addModal = null;
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
function openModal() {
    if (!addModal) {
        addModal = new Modal(
            document.getElementById("addTrekModal")
        );
    }
    if (!isEditing.value) {
        trekForm.value = { ...initialForm };
        editingId.value = null;
    }
    addModal.show();
}
function closeModal() {
    if (addModal) {
        addModal.hide();
    }
    trekForm.value = { ...initialForm };
    isEditing.value = false;
    editingId.value = null;
}
function closeAssignModal() {
    if (assignModal) {
        assignModal.hide();
    }
    selectedStaff.value = "";
    selectedTrek.value = null;
}
function closeDetailsModal() {
    if (detailsModal) {
        detailsModal.hide();
    }
    viewTrek.value = null;
}
function editTrek(trek) {
    isEditing.value = true;
    editingId.value = trek.id;
    trekForm.value = {
        name: trek.name,
        location: trek.location,
        description: trek.description,
        difficulty: trek.difficulty,
        duration: trek.duration,
        start_date: trek.start_date,
        end_date: trek.end_date,
    };
    openModal();
}
function openAssignModal(trek) {
    selectedTrek.value = trek;
    selectedStaff.value = trek.staff_id;
    if (!assignModal) {
        assignModal = new Modal(
            document.getElementById("assignStaffModal")
        );
    }
    loadActiveStaff();
    assignModal.show();
}
function openDetailsModal(trek) {
    console.log("Selected Trek:", trek);
    viewTrek.value = trek;
    console.log("viewTrek:", viewTrek.value);
    if (!detailsModal) {
        detailsModal = new Modal(
            document.getElementById("trekDetailsModal")
        );
    }
    detailsModal.show();
}
async function loadTreks() {
    try {
        const response = await api.get("/admin/treks");
        treks.value = response.data.data;
    }
    catch (err) {
        console.error(err);
    }
}
async function loadActiveStaff() {
    try {
        const response = await api.get("/admin/staff/active");
        activeStaff.value = response.data.data;
    }
    catch (err) {
        console.error(err);
        alert(
            err.response?.data?.message ||
            "Unable to load staff."
        );
    }
}
async function saveTrek() {
    if (trekForm.value.duration < 1) {
        alert("Duration must be at least 1 day.");
        return;
    }
    try {
        if(isEditing.value){
            await api.put(
                `/admin/treks/${editingId.value}`, trekForm.value
            );
        }
        else{
            await api.post("/admin/treks", trekForm.value);
        }
        closeModal();
        await loadTreks();
    }
    catch (err) {
        console.error(err);
    }
}
async function toggleStatus(trek) {
    const newStatus =
        trek.status === "Inactive"
            ? "Pending"
            : "Inactive";
    try {
        await api.put(`/admin/treks/${trek.id}/toggle`);
        await loadTreks();
    }
    catch (err) {
        console.error(err);
    }
}
async function assignStaff() {
    try {
        await api.put(
            `/admin/treks/${selectedTrek.value.id}/assign-staff`,
            {
                staff_id: selectedStaff.value
            }
        );
        alert(
            selectedStaff.value
            ? "Staff assigned successfully."
            : "Staff removed successfully."
        );
        closeAssignModal();
        await loadTreks();
    }
    catch (err) {
        console.error(err);
        alert(
            err.response?.data?.message ||
            "Failed to assign staff."
        );
    }
}
onMounted(loadTreks);
</script>