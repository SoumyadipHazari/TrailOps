<template>
    <nav class="navbar navbar-expand-lg shadow-sm px-4 py-2 custom-navbar">

        <div class="d-flex align-items-center">

            <i class="bi bi-signpost-split-fill fs-3 text-warning me-3"></i>

            <div>

                <div class="navbar-brand fw-bold fs-3 mb-0">
                    TrailOps
                </div>

                <small class="text-light opacity-75">
                    Smart Trekking Management Platform
                </small>

            </div>

        </div>

        <div class="ms-auto">
            <LogoutButton />
        </div>

    </nav>
</template>

<script setup>
import LogoutButton from "./LogoutButton.vue";
</script>

<style scoped>

.custom-navbar{
    background: linear-gradient(
        90deg,
        #1f3d2b,
        #2f5d43
    );
}

.navbar-brand{
    color:white !important;
    line-height:1;
}

</style>