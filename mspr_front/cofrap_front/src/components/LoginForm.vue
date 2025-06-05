<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card class="pa-8" elevation="8" rounded="xl">
          <!-- Logo -->
          <div class="text-center mb-6">
            <v-img
              src="@/assets/lacofrap.png"
              alt="Logo"
              max-width="60"
              class="mx-auto mb-2"
            />
          </div>
          <!-- Titre -->
          <div class="text-center mb-6">
            <h2 class="font-weight-bold mb-1">Log into your account</h2>
          </div>
          <!-- Formulaire -->
          <v-form @submit.prevent="onSubmit" ref="form" v-model="formValid">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-inner-icon="mdi-account"
              :rules="[v => !!v || 'Username is required']"
              outlined
              dense
              class="mb-3"
              autocomplete="username"
            />
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              prepend-inner-icon="mdi-lock"
              :rules="[v => !!v || 'Password is required']"
              outlined
              dense
              class="mb-3"
              autocomplete="current-password"
            />
            <v-text-field
              v-model="code2fa"
              label="2FA code"
              prepend-inner-icon="mdi-shield-key"
              :rules="[v => !!v || '2FA code is required']"
              outlined
              dense
              class="mb-3"
              autocomplete="one-time-code"
            />
            <!-- Remember me & Forgot password -->
            <v-row align="center" class="mb-4">
              <v-col cols="6">
                <v-checkbox
                  v-model="remember"
                  label="Remember me"
                  dense
                  hide-details
                />
              </v-col>
              <v-col cols="6" class="text-right">
                <v-btn variant="text" color="primary" class="pa-0" @click="forgotPassword">
                  Forgot password?
                </v-btn>
              </v-col>
            </v-row>
            <!-- Erreur -->
            <v-alert
              v-if="errorMessage"
              type="error"
              dense
              class="mb-3"
              border="start"
            >
              {{ errorMessage }}
            </v-alert>
            <!-- Bouton -->
            <v-btn
              color="primary"
              type="submit"
              block
              large
              :loading="loading"
              :disabled="!formValid || loading"
              class="mb-2"
            >
              Log In
            </v-btn>
          </v-form>
          <!-- Lien vers inscription -->
          <div class="text-center mt-4">
            <span>Don't have an account?
              <v-btn variant="text" color="primary" class="pa-0" @click="goToRegister">
                Sign up
              </v-btn>
            </span>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const code2fa = ref('')
const remember = ref(false)
const errorMessage = ref('')
const loading = ref(false)
const formValid = ref(false)

function onSubmit() {
  errorMessage.value = ''
  loading.value = true
  // Remplace par ton appel API
  setTimeout(() => {
    loading.value = false
    if (!username.value || !password.value || !code2fa.value) {
      errorMessage.value = 'All fields are required.'
    } else if (username.value !== 'user' || password.value !== 'password' || code2fa.value !== '123456') {
      errorMessage.value = 'Invalid credentials or 2FA code.'
    } else {
      // Succès
      router.push('/')
    }
  }, 1000)
}
function forgotPassword() {
  alert('Password reset link sent!')
}
function goToRegister() {
  router.push('/register')
}
</script>
