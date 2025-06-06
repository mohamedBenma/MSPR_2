<template>
  <v-app>
    <!-- ░░ HEADER ░░ -->
    <v-app-bar color="white" height="72" flat elevation="1" class="px-6">
      <!-- Logo inside an elevated avatar for cleaner look -->
      <v-avatar
        size="48"
        rounded="lg"
        class="elevation-2 mr-4"
        style="overflow: hidden"
      >
        <v-img :src="logo" aspect-ratio="1" cover />
      </v-avatar>

      <!-- Small product name next to logo (optional) -->
      <span class="text-h6 font-weight-medium">COFRAP&nbsp;Cloud</span>

      <v-spacer />

      <v-btn variant="plain" color="primary" @click="goToLogin">Log in</v-btn>
      <v-btn class="ml-2" color="primary" elevation="0" @click="goToRegister">
        Sign up
      </v-btn>
    </v-app-bar>

    <!-- ░░ HERO ░░ -->
    <v-parallax
      height="520"
      :src="heroImg"
      gradient="to bottom, rgba(0,0,0,.45), rgba(0,0,0,.9)"
      style="mask-image: linear-gradient(to bottom, black 82%, transparent)"
    >
      <v-container
        class="fill-height d-flex flex-column justify-center text-center"
      >
        <h1 class="display-1 font-weight-bold text-white mb-4">
          COFRAP&nbsp;Cloud&nbsp;Access
        </h1>
        <p class="text-h6 text-white mb-8">
          Secure • Inclusive • Serverless<br />
          Manage credentials without compromise.
        </p>

        <div>
          <v-btn
            size="large"
            color="primary"
            elevation="2"
            class="mr-4"
            @click="goToRegister"
          >
            Start free trial
          </v-btn>
          <v-btn
            size="large"
            variant="outlined"
            color="white"
            @click="scrollTo('features')"
          >
            Learn more
          </v-btn>
        </div>
      </v-container>
    </v-parallax>

    <!-- ░░ PILLARS ░░ -->
    <v-container id="features" class="py-16">
      <h2 class="text-h4 font-weight-bold text-center mb-10">
        What makes us different
      </h2>

      <v-row justify="center" dense>
        <v-col
          v-for="p in pillars"
          :key="p.title"
          cols="12"
          sm="6"
          md="4"
          class="d-flex"
        >
          <v-card
            color="primary"
            theme="dark"
            elevation="2"
            class="pa-6 flex-grow-1"
          >
            <v-icon :icon="p.icon" size="48" class="mb-4" />
            <h3 class="text-h6 font-weight-bold mb-2">{{ p.title }}</h3>
            <p>{{ p.desc }}</p>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- ░░ USE-CASES ░░ -->
    <v-container class="py-16">
      <h2 class="text-h4 font-weight-bold text-center mb-10">
        Real-world use cases
      </h2>

      <v-row>
        <v-col v-for="c in cases" :key="c.title" cols="12" md="4">
          <v-card elevation="4">
            <v-img :src="c.img" height="180" cover />
            <v-card-title class="font-weight-bold">{{ c.title }}</v-card-title>
            <v-card-text>{{ c.desc }}</v-card-text>
            <v-card-actions>
              <v-btn variant="text" color="primary">Explore</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- ░░ CTA ░░ -->
    <v-container class="py-16 text-center">
      <h2 class="text-h4 font-weight-bold mb-4">
        Ready to secure your access?
      </h2>
      <p class="mb-8">
        Deploy our OpenFaaS functions in minutes and start your proof-of-concept
        today.
      </p>
      <v-btn size="x-large" color="primary" elevation="2" @click="goToRegister">
        Create my account
      </v-btn>
    </v-container>

    <!-- ░░ FOOTER ░░ -->
    <v-footer class="py-6" color="#0d1b2a" theme="dark">
      <v-container>
        <v-row align="center" justify="space-between">
          <span
            >&copy; {{ new Date().getFullYear() }} COFRAP • All rights
            reserved</span
          >
          <v-btn
            variant="text"
            size="small"
            color="primary"
            href="https://openfaas.com"
            target="_blank"
          >
            Powered by OpenFaaS
          </v-btn>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import logo from "@/assets/logo.png"; //  ▶ put your logo in src/assets

/* router shortcuts */
const router = useRouter();
const goToLogin = () => router.push("/login");
const goToRegister = () => router.push("/register");
const scrollTo = (id) =>
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });

/* hero image chosen for reliability */
const heroImg =
  "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&w=1600&q=80";

/* pillars -- EN */
const pillars = ref([
  {
    icon: "mdi-shield-lock",
    title: "Strong security",
    desc: "24-char passwords, unique QR codes, encrypted storage & mandatory 2-factor auth.",
  },
  {
    icon: "mdi-cloud-sync",
    title: "Serverless scalability",
    desc: "OpenFaaS “scale-to-zero” functions on Kubernetes, billed only when used.",
  },
  {
    icon: "mdi-account-heart",
    title: "Inclusive experience",
    desc: "Accessible UI, automated credential rotation, multi-cultural onboarding.",
  },
]);

/* use-case cards with working photos */
const cases = ref([
  {
    img: "https://www.freshbooks.com/wp-content/uploads/2022/02/types-of-accounts.jpg",
    title: "Instant onboarding",
    desc: "Create secure accounts for 1,000 employees in under a minute.",
  },
  {
    img: "https://images.pexels.com/photos/3184301/pexels-photo-3184301.jpeg?auto=compress&cs=tinysrgb&w=800",
    title: "6-month rotation",
    desc: "Stay compliant with automatic password & TOTP renewal every six months.",
  },
  {
    img: "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=800",
    title: "Audit & compliance",
    desc: "Export full authentication logs for ISO 27001 / GDPR in one click.",
  },
]);
</script>

<style scoped>
h1,
h2 {
  letter-spacing: -0.5px;
}
</style>
