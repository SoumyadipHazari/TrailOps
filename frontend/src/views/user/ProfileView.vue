<template>

    <Navbar />

    <div class="container-fluid">

        <div class="row">

            <div class="col-md-2 p-0">
                <Sidebar />
            </div>

            <div class="col-md-10 p-4">

                <h2>My Profile</h2>

                <p class="text-muted">
                    Update your account information.
                </p>

                <hr>

                <div class="card shadow">

                    <div class="card-body">

                        <div class="text-center mb-4">

                            <div class="display-4">
                                👤
                            </div>

                            <h5 class="mt-2">
                                {{ profile.name }}
                            </h5>

                            <p class="text-muted">
                                {{ formatUserId(profile.id) }}
                            </p>

                        </div>

                        <div class="mb-3">

                            <label class="form-label">
                                Name
                            </label>

                            <input
                                class="form-control"
                                v-model="profile.name"
                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">
                                Email
                            </label>

                            <input
                                class="form-control"
                                v-model="profile.email"
                                readonly
                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">
                                Phone
                            </label>

                            <input
                                type="tel"
                                class="form-control"
                                v-model="profile.phone"
                                maxlength="10"
                                inputmode="numeric"
                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">
                                New Password
                            </label>

                            <div class="input-group">
                                <input
                                    :type="showPassword ? 'text' : 'password'"
                                    class="form-control"
                                    v-model="password"
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
                        </div>

                        <div class="mb-4">

                            <label class="form-label">
                                Confirm Password
                            </label>

                            <div class="input-group">

                                <input
                                    :type="showConfirmPassword ? 'text' : 'password'"
                                    class="form-control"
                                    v-model="confirmPassword"
                                    autocomplete="new-password"
                                >

                                <button
                                    class="btn btn-outline-secondary"
                                    type="button"
                                    @click="showConfirmPassword = !showConfirmPassword"
                                >
                                    <i
                                        :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                                    ></i>
                                </button>

                            </div>

                        </div>

                        <button
                            class="btn btn-secondary me-2"
                            @click="loadProfile"
                        >
                            Reset
                        </button>
                        <button
                            class="btn btn-primary"
                            @click="saveProfile"
                        >
                            Save Changes
                        </button>

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

const profile = ref({
    id: "",
    name: "",
    email: "",
    phone: ""
});

const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function formatUserId(id){

    return `U${String(id).padStart(3,"0")}`;

}

function validPhone(phone) {
    return /^\d{10}$/.test(phone);
}

function validPassword(password) {
    return password.length >= 4;
}

async function loadProfile(){

    try{

        const response = await api.get("/user/profile");

        profile.value = response.data.data;
        password.value = "";
        confirmPassword.value = "";

    }

    catch(err){

        alert(
            err.response?.data?.message ||
            "Unable to load profile."
        );

    }

}

async function saveProfile(){

    if(
        password.value &&
        password.value !== confirmPassword.value
    ){
        alert("Passwords do not match.");
        return;
    }
    if (!validPhone(profile.value.phone)) {
        alert("Phone number must contain exactly 10 digits.");
        return;
    }

    if (
        password.value &&
        !validPassword(password.value)
    ){
        alert("Password must be at least 4 characters long.");
        return;
    }
    const payload = {
        name: profile.value.name,
        phone: profile.value.phone
    };

    if(password.value){
        payload.password = password.value;
    }

    try{

        await api.put(
            "/user/profile",
            payload
        );

        alert("Profile updated successfully.");

        password.value = "";
        confirmPassword.value = "";

        await loadProfile();

    }

    catch(err){

        alert(
            err.response?.data?.message ||
            "Unable to update profile."
        );

    }

}

onMounted(loadProfile);

</script>