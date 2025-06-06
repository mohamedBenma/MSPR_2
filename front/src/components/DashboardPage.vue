<!-- src/views/Dashboard.vue -->
<template>
  <v-app>
    <!-- ── TOP BAR ───────────────────────────────────── -->
    <v-app-bar color="primary" dark dense>
      <!-- Logo on the left -->
      <v-img
        src="@/assets/logo.png"
        alt="COFRAP Logo"
        height="32"
        width="150"
        class="mr-3"
      />
      <v-toolbar-title class="font-weight-bold">
        COFRAP Dashboard
      </v-toolbar-title>

      <v-spacer />

      <!-- USER BADGE -->
      <v-chip
        color="white"
        text-color="primary"
        class="ma-2 font-weight-medium"
      >
        <v-icon left>mdi-account-circle</v-icon>
        {{ username }}
      </v-chip>

      <!-- LOGOUT BUTTON -->
      <v-btn text color="white" class="ml-2" @click="logout"> Logout </v-btn>
    </v-app-bar>

    <!-- ── MAIN CONTENT ───────────────────────────────── -->
    <v-main class="bg-page">
      <v-container class="py-8">
        <!-- Greeting and Clock Row -->
        <v-row align="center" justify="space-between" class="mb-8">
          <v-col cols="12" sm="6">
            <h2 class="text-h4 font-weight-bold">
              Welcome back, {{ username }}!
            </h2>
            <p class="text-subtitle-1 text-medium">
              Here's a quick glance at your dashboard.
            </p>
          </v-col>

          <v-col cols="12" sm="4">
            <v-card
              class="card d-flex flex-column align-center justify-center"
              elevation="2"
            >
              <v-icon color="primary" size="32">mdi-clock-outline</v-icon>
              <div class="mt-2 text-h5 font-weight-medium">{{ time }}</div>
              <div class="text-subtitle-2 text-medium">{{ date }}</div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Simple Info Cards -->
        <v-row dense>
          <v-col cols="12" md="4">
            <v-card class="card text-center pa-6" elevation="2">
              <v-icon color="primary" size="36" class="mb-2"
                >mdi-information-outline</v-icon
              >
              <h3 class="text-h6 font-weight-medium mb-2">Account Status</h3>
              <p class="text-subtitle-2">Active</p>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="card text-center pa-6" elevation="2">
              <v-icon color="primary" size="36" class="mb-2"
                >mdi-email-check-outline</v-icon
              >
              <h3 class="text-h6 font-weight-medium mb-2">Notifications</h3>
              <p class="text-subtitle-2">You have 3 unread messages</p>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="card text-center pa-6" elevation="2">
              <v-icon color="primary" size="36" class="mb-2"
                >mdi-server-network</v-icon
              >
              <h3 class="text-h6 font-weight-medium mb-2">System Load</h3>
              <p class="text-subtitle-2">Operational</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
  
  <script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

/* ── ROUTER & LOGOUT ───────────────────────────────── */
const router = useRouter();
function logout() {
  // Clear stored username and redirect to main page
  localStorage.removeItem("cofrapUsername");
  router.push("/");
}

/* ── USERNAME ───────────────────────────────────── */
const username = ref(localStorage.getItem("cofrapUsername") || "guest");
if (!username.value) {
  username.value = "guest";
}

/* ── CLOCK ──────────────────────────────────────── */
const time = ref("");
const date = ref("");
let timer;

/** Update both time and date each second */
function updateClock() {
  const now = new Date();
  time.value = now.toLocaleTimeString(undefined, { hour12: false });
  date.value = now.toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

onMounted(() => {
  updateClock();
  timer = setInterval(updateClock, 1000);
});

onBeforeUnmount(() => {
  clearInterval(timer);
});
</script>
  
  <style scoped>
/* ── COLOURS & LAYOUT ───────────────────────────── */
:root {
  --card-bg: rgb(var(--v-theme-surface) / 1);
  --card-radius: 12px;
  --card-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  --page-bg: #f5f7fa;
  --text-medium: #6b6b6b;
}

.bg-page {
  background-color: var(--page-bg);
  min-height: 100vh;
}

.card {
  background-color: var(--card-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
}

/* Heading spacing */
.text-h4 {
  margin-bottom: 8px;
}

/* Secondary text color */
.text-medium {
  color: var(--text-medium);
}

/* Icon bottom margin override */
.v-icon.mb-2 {
  margin-bottom: 12px !important;
}

/* Container vertical padding */
.v-container.py-8 {
  padding-top: 32px !important;
  padding-bottom: 32px !important;
}
</style>
  