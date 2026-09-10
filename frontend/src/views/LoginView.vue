<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4" style="width: 420px;">
      <h2 class="text-center mb-4">TrailOps Trekking Management</h2>

      <form @submit.prevent="login">

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            v-model="email"
            required
          />
        </div>

        <div class="mb-4">
            <label class="form-label">Password</label>
            <div class="input-group">

                <input
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    v-model="password"
                    required
                />

                <button
                    class="btn btn-outline-secondary"
                    type="button"
                    @click="showPassword = !showPassword"
                >
                    {{ showPassword ? "Hide" : "Show" }}
                </button>

            </div>
        </div>

        <button
          class="btn btn-primary w-100"
          type="submit"
        >
          Login
        </button>

      </form>

      <p class="text-center mt-3">
        Don't have an account?

        <router-link to="/register">
          Register
        </router-link>

      </p>

      <div
        v-if="error"
        class="alert alert-danger mt-3"
      >
        {{ error }}
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const email = ref("");
const password = ref("");
const error = ref("");
const showPassword = ref(false);

async function login() {

    error.value = "";

    try {

        const response = await api.post("/auth/login", {
            email: email.value,
            password: password.value
        });
        console.log(response.data);

        const role = response.data.role;

        if (role === "admin") {
            console.log("Going to admin...");
            router.push("/admin/dashboard");
        }

        else if (role === "staff") {
            console.log("Going to staff...");
            router.push("/staff/dashboard");
        }

        else if (role === "user") {
            console.log("Going to user...");
            router.push("/user/dashboard");
        }

    }

    catch (err) {

        if (err.response) {
            error.value = err.response.data.message;
        }

        else {
            error.value = "Unable to connect to server.";
        }

    }

}

</script>