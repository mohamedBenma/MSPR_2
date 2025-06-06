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
              :disabled="loading"
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
              :disabled="loading"
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
              :disabled="loading"
            />
            <!-- Remember me & Forgot password -->
            <v-row align="center" class="mb-4">
              <v-col cols="6">
                <v-checkbox
                  v-model="remember"
                  label="Remember me"
                  dense
                  hide-details
                  :disabled="loading"
                />
              </v-col>
              <v-col cols="6" class="text-right">
                <v-btn variant="text" color="primary" class="pa-0" @click="forgotPassword" :disabled="loading">
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
            <!-- Message de succès -->
            <v-alert
              v-if="successMessage"
              type="success"
              dense
              class="mb-3"
              border="start"
            >
              {{ successMessage }}
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
              <v-btn variant="text" color="primary" class="pa-0" @click="goToRegister" :disabled="loading">
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
const successMessage = ref('')
const loading = ref(false)
const formValid = ref(false)

// URL de votre gateway OpenFaaS (à adapter selon votre configuration)
//const OPENFAAS_GATEWAY = 'http://127.0.0.1:8080' // ou votre URL réelle

async function onSubmit() {
  errorMessage.value = ''
  successMessage.value = ''
  loading.value = true
  
  try {
    // Appel à votre fonction OpenFaaS d'authentification
    const response = await fetch('/function/auth-user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        code: code2fa.value
      })
    })

    const data = await response.json()
    
    if (response.status === 200) {
      // Succès
      successMessage.value = data.message
      setTimeout(() => {
        router.push('/') // Redirection vers la page d'accueil
      }, 1500)
      
    } else if (response.status === 403) {
      // Compte expiré
      errorMessage.value = data.error + ' Souhaitez-vous renouveler vos identifiants ?'
      // Optionnel : proposer un bouton pour aller vers la page de renouvellement
      
    } else if (response.status === 401) {
      // Identifiants incorrects
      errorMessage.value = data.error
      
    } else if (response.status === 404) {
      // Utilisateur introuvable
      errorMessage.value = data.error
      
    } else {
      // Autres erreurs
      errorMessage.value = data.error || 'Erreur lors de la connexion'
    }
    
  } catch (error) {
    console.error('Erreur lors de la connexion:', error)
    errorMessage.value = 'Erreur de connexion au serveur. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}

function forgotPassword() {
  router.push('/renew') // Redirection vers page de renouvellement
}

function goToRegister() {
  router.push('/register')
}
</script>
