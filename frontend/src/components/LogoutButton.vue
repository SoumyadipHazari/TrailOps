<template>
    <button
        class="btn btn-danger"
        @click="logout"
    >
        Logout
    </button>
</template>

<script setup>
import api from "../services/api";
import { useRouter } from "vue-router";

const router = useRouter();

async function logout() {

    try {

        await api.post("/auth/logout");

        router.push("/login");

    }

    catch (err) {

        console.error(err);

    }

}
</script>