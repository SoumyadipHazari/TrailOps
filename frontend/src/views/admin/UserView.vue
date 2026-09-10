<template>
    <Navbar />
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0">
                <Sidebar />
            </div>
            <div class="col-md-10 p-4">
                <h2>Users</h2>
                <p class="text-muted">
                    View and manage all registered users.
                </p>
                <hr>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input
                            class="form-control"
                            type="text"
                            placeholder="Search by name or email..."
                            v-model="search"
                        >
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th>User ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Registered</th>
                                <th>Status</th>
                                <th class="text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="user in filteredUsers"
                                :key="user.id"
                            >
                                <td>
                                    {{ formatUserId(user.id) }}
                                </td>
                                <td>
                                    {{ user.name }}
                                </td>
                                <td>
                                    {{ user.email }}
                                </td>
                                <td>
                                    {{ user.phone }}
                                </td>
                                <td>
                                    {{ formatDate(user.created_at) }}
                                </td>
                                <td>
                                    <span
                                        class="badge"
                                        :class="user.status === 'active'
                                            ? 'bg-success'
                                            : 'bg-danger'"
                                    >
                                        {{ user.status }}
                                    </span>
                                </td>
                                <td class="text-center">
                                    <button
                                        class="btn btn-sm"
                                        :class="user.status === 'active'
                                            ? 'btn-danger'
                                            : 'btn-success'"
                                        @click="toggleStatus(user)"
                                    >
                                        {{
                                            user.status === "active"
                                                ? "Deactivate"
                                                : "Activate"
                                        }}
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div
                    v-if="filteredUsers.length === 0"
                    class="text-center mt-5"
                >
                    <h4>No users found.</h4>
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
const users = ref([]);
const search = ref("");
const filteredUsers = computed(() => {
    if (!search.value) {
        return users.value;
    }
    const keyword = search.value.toLowerCase();
    return users.value.filter(user =>
        user.name.toLowerCase().includes(keyword) ||
        user.email.toLowerCase().includes(keyword)
    );
});
async function loadUsers(){
    try{
        const response = await api.get("/admin/users");
        users.value = response.data.data;
    }
    catch(err){
        alert(
            err.response?.data?.message ||
            "Unable to load users."
        );
    }
}
function formatUserId(id){
    return `U${String(id).padStart(3,"0")}`;
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
async function toggleStatus(user){
    const newStatus =
        user.status === "active"
            ? "inactive"
            : "active";
    const action =
        newStatus === "inactive"
            ? "Deactivate"
            : "Activate";
    if(
        !confirm(`${action} this user?`)
    ) return;
    try{
        await api.put(
            `/admin/users/${user.id}/status`,
            {
                status: newStatus
            }
        );
        alert(`User ${action.toLowerCase()}d successfully.`);
        await loadUsers();
    }
    catch(err){
        alert(
            err.response?.data?.message ||
            "Operation failed."
        );
    }
}
onMounted(loadUsers);
</script>