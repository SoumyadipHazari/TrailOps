<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4" style="width: 500px;">
      <h2 class="text-center mb-4">Create Account</h2>

      <form @submit.prevent="register">

        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input
            type="text"
            class="form-control"
            v-model="name"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            v-model="email"
            required
            autocomplete="new-email"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input
            type="tel"
            class="form-control"
            v-model="phone"
            maxlength="10"
            inputmode="numeric"
            required
          />
        </div>

        <div class="mb-3">

            <label class="form-label">
                Password
            </label>

            <div class="input-group">

                <input
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    v-model="password"
                    required
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
                    required
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
          class="btn btn-success w-100"
          type="submit"
        >
          Register
        </button>

      </form>

      <p class="text-center mt-3">
        Already have an account?

        <router-link to="/login">
          Login
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
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const name = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");

const error = ref("");
function validPhone(phone) {
    return /^\d{10}$/.test(phone);
}

function validPassword(password) {
    return password.length >= 4;
}

async function register() {

    error.value = "";
    if (password.value !== confirmPassword.value) {
        error.value = "Passwords do not match.";
        return;
    }

    if (!validPhone(phone.value)) {
        error.value = "Phone number must contain exactly 10 digits.";
        return;
    }

    if (!validPassword(password.value)) {
        error.value = "Password must be at least 4 characters long.";
        return;
    }

    try {

        await api.post("/auth/register", {
            name: name.value,
            email: email.value,
            phone: phone.value,
            password: password.value
        });

        alert("Registration successful!");
        name.value = "";
        email.value = "";
        phone.value = "";
        password.value = "";
        confirmPassword.value = "";
        router.push("/login");

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