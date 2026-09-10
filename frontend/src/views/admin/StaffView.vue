<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>Staff Management</h2>
                    <button
                        class="btn btn-success"
                        @click="addStaff"
                    >
                        Add Staff
                    </button>
                </div>
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Experience</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="staff in staffList"
                            :key="staff.id"
                        >
                            <td>{{ formatId("S", staff.id) }}</td>
                            <td>{{ staff.name }}</td>
                            <td>{{ staff.email }}</td>
                            <td>{{ staff.phone }}</td>
                            <td>{{ staff.experience || 0 }} Years</td>
                            <td>
                                <span
                                    class="badge"
                                    :class="{
                                        'bg-success': staff.status === 'active',
                                        'bg-danger': staff.status === 'inactive'
                                    }"
                                >
                                    {{ staff.status }}
                                </span>
                            </td>
                            <td>
                                <button
                                    class="btn btn-primary btn-sm me-2"
                                    @click="editStaff(staff)"
                                >
                                    Edit
                                </button>
                                <button
                                    class="btn btn-sm"
                                    :class="staff.status === 'inactive'
                                        ? 'btn-success'
                                        : 'btn-danger'"
                                    @click="toggleStatus(staff)"
                                >
                                    {{ staff.status === "inactive"
                                        ? "Activate"
                                        : "Deactivate" }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div
        class="modal fade"
        id="addStaffModal"
        tabindex="-1"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        {{ isEditing ? "Edit Staff" : "Add Staff" }}
                    </h5>
                    <button
                        class="btn-close"
                        type="button"
                        @click="closeModal"
                    ></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label>Name</label>
                        <input
                            class="form-control"
                            v-model="staffForm.name"
                        >
                    </div>
                    <div class="mb-3">
                        <label>Email</label>
                        <input
                            type="email"
                            class="form-control"
                            v-model="staffForm.email"
                            :disabled="isEditing"
                        >
                    </div>
                    <div class="mb-3">
                        <label>Phone</label>
                        <input
                            type="tel"
                            class="form-control"
                            v-model="staffForm.phone"
                            maxlength="10"
                            inputmode="numeric"
                        >
                    </div>
                    <div class="mb-3">
                        <label>
                            {{ isEditing ? "New Password" : "Password" }}
                        </label>
                        <div class="input-group">
                            <input
                                :type="showPassword ? 'text' : 'password'"
                                class="form-control"
                                v-model="staffForm.password"
                                :placeholder="
                                    isEditing
                                        ? 'Leave blank to keep current password'
                                        : 'Enter password'
                                "
                                autocomplete="new-password"
                            >

                            <button
                                class="btn btn-outline-secondary"
                                type="button"
                                @click="showPassword = !showPassword"
                            >
                                <i
                                    :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                                ></i>
                            </button>

                        </div>

                        <small class="text-muted">
                            Password must contain at least 4 characters.
                        </small>
                        <small
                            v-if="isEditing"
                            class="text-muted"
                        >
                            Leave empty if you don't want to change the password.
                        </small>
                    </div>
                    <div class="mb-3">
                        <label>Experience</label>
                        <input
                            type="number"
                            class="form-control"
                            min = "0"
                            v-model.number="staffForm.experience"
                        >
                    </div>
                    <div
                        class="mb-3"
                        v-if="isEditing"
                    >
                        <label>Status</label>
                        <select
                            class="form-select"
                            v-model="staffForm.status"
                        >
                            <option value="active">active</option>
                            <option value="inactive">inactive</option>
                        </select>
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
                        @click="saveStaff"
                    >
                        {{ isEditing ? "Update Staff" : "Save Staff" }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { Modal } from "bootstrap";
import api from "../../services/api";
import Navbar from "../../components/Navbar.vue";
import Sidebar from "../../components/Sidebar.vue";
const staffList = ref([]);
const initialForm = {
    name: "",
    email: "",
    phone: "",
    password: "",
    experience: 0,
    status: "active"
};
const staffForm = ref({ ...initialForm });
const isEditing = ref(false);
const editingId = ref(null);
const showPassword = ref(false);
let addModal = null;
function formatId(prefix, id) {
    return `${prefix}${String(id).padStart(3, "0")}`;
}
function validPhone(phone) {
    return /^\d{10}$/.test(phone);
}

function validPassword(password) {
    return password.length >= 4;
}
function addStaff() {

    isEditing.value = false;
    editingId.value = null;
    showPassword.value = false;

    staffForm.value = {
        ...initialForm
    };

    openModal();

}
function openModal() {
    if (!addModal) {
        addModal = new Modal(
            document.getElementById("addStaffModal")
        );
    }
    if (!isEditing.value) {
        staffForm.value = { ...initialForm };
        editingId.value = null;
        showPassword.value = false;
    }
    addModal.show();
}
function closeModal() {
    if (addModal) {
        addModal.hide();
    }
    staffForm.value = { ...initialForm };
    isEditing.value = false;
    editingId.value = null;
    showPassword.value = false;
}
function editStaff(staff) {
    isEditing.value = true;
    editingId.value = staff.id;
    staffForm.value = {
        name: staff.name,
        email: staff.email,
        phone: staff.phone,
        password: "",
        experience: staff.experience,
        status: staff.status
    };
    openModal();
}
async function loadStaff() {
    try {
        const response = await api.get("/admin/staff");
        staffList.value = response.data.data;
    }
    catch (err) {
        console.error(err);
        alert(
            err.response?.data?.message ||
            "Something went wrong."
        );
    }
}
async function saveStaff() {
    if (!validPhone(staffForm.value.phone)) {
        alert("Phone number must contain exactly 10 digits.");
        return;
    }

    if (
        staffForm.value.password &&
        !validPassword(staffForm.value.password)
    ) {
        alert("Password must be at least 4 characters long.");
        return;
    }
    
    try {
        if (isEditing.value) {
            const payload = {
                name: staffForm.value.name,
                phone: staffForm.value.phone,
                experience: staffForm.value.experience,
                status: staffForm.value.status
            };
            if (staffForm.value.password) {
                payload.password = staffForm.value.password;
            }
            await api.put(
                `/admin/staff/${editingId.value}`,
                payload
            );
        } else {
            await api.post(
                "/admin/staff",
                staffForm.value
            );
        }
        await loadStaff();
        alert(
            isEditing.value
                ? "Staff updated successfully."
                : "Staff created successfully."
        );
        closeModal();
    }
    catch (err) {
        console.error(err);
        alert(
            err.response?.data?.message ||
            "Something went wrong."
        );
    }
}
async function toggleStatus(staff) {
    const newStatus =
        staff.status === "inactive"
            ? "active"
            : "inactive";
    try {
        await api.put(
            `/admin/staff/${staff.id}`,
            {
                ...staff,
                status: newStatus
            }
        );
        await loadStaff();
    }
    catch (err) {
        console.error(err);
        alert(
            err.response?.data?.message ||
            "Something went wrong."
        );
    }
}
onMounted(loadStaff);
</script>