<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card class="pa-8" elevation="8" rounded="xl">
          <!-- Logo -->
          <div class="text-center mb-6">
            <v-img
              src="@/assets/logo.png"
              alt="Logo"
              max-width="60"
              class="mx-auto mb-2"
            />
          </div>
          <!-- Titre -->
          <div class="text-center mb-6">
            <h2 class="font-weight-bold mb-1">Create your account</h2>
          </div>
          
          <!-- Formulaire -->
          <v-form @submit.prevent="createAccount" ref="form" v-model="formValid">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-inner-icon="mdi-account"
              :rules="[v => !!v || 'Username is required']"
              outlined
              dense
              class="mb-3"
              :disabled="loading"
            />
            
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
            
            <v-btn
              color="primary"
              type="submit"
              block
              large
              :loading="loading"
              :disabled="!formValid || loading"
              class="mb-2"
            >
              Create Account
            </v-btn>
          </v-form>
          
          <!-- Section QR Codes générés -->
          <v-expand-transition>
            <div v-if="accountCreated" class="mt-6">
              <v-alert type="success" class="mb-4">
                {{ serverMessage }}
              </v-alert>
              
              <!-- Mot de passe généré -->
              <v-card outlined class="mb-4 pa-4">
                <h3 class="mb-3">🔐 Your Password</h3>
                <v-text-field
                  :value="generatedPassword"
                  label="Generated Password"
                  readonly
                  outlined
                  dense
                  append-icon="mdi-content-copy"
                  @click:append="copyToClipboard(generatedPassword)"
                />
                
                <!-- QR Code du mot de passe -->
                <div class="text-center mb-3">
                  <p class="text-body-2 mb-2">Scan this QR code to save your password:</p>
                  <img 
                    :src="passwordQrDisplay" 
                    alt="Password QR Code"
                    class="qr-code-image"
                  />
                </div>
              </v-card>
              
              <!-- Secret 2FA -->
              <v-card outlined class="mb-4 pa-4">
                <h3 class="mb-3">📱 Two-Factor Authentication</h3>
                <v-text-field
                  :value="mfaSecret"
                  label="2FA Secret"
                  readonly
                  outlined
                  dense
                  append-icon="mdi-content-copy"
                  @click:append="copyToClipboard(mfaSecret)"
                />
                
                <!-- QR Code 2FA -->
                <div class="text-center mb-3">
                  <p class="text-body-2 mb-2">Scan this QR code with your authenticator app:</p>
                  <img 
                    :src="mfaQrDisplay" 
                    alt="2FA QR Code"
                    class="qr-code-image"
                  />
                </div>
              </v-card>
              
              <v-btn 
                color="success" 
                block 
                large
                @click="goToLogin"
                class="mt-4"
              >
                I've saved my credentials - Go to Login
              </v-btn>
            </div>
          </v-expand-transition>
          
          <!-- Lien vers connexion -->
          <div class="text-center mt-4">
            <span>Already have an account?
              <v-btn variant="text" color="primary" class="pa-0" @click="goToLogin">
                Log in
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

// Variables réactives
const username = ref('')
const loading = ref(false)
const formValid = ref(false)
const errorMessage = ref('')
const accountCreated = ref(false)
const serverMessage = ref('')
const generatedPassword = ref('')
const mfaSecret = ref('')
const passwordQrDisplay = ref('')
const mfaQrDisplay = ref('')

// URL de votre gateway OpenFaaS (à adapter selon votre configuration)
const OPENFAAS_GATEWAY = 'http://127.0.0.1:8080' // ou votre URL réelle

async function createAccount() {
  errorMessage.value = ''
  loading.value = true
  
  try {
    // Appel à votre fonction OpenFaaS de création d'utilisateur
    const response = await fetch(`${OPENFAAS_GATEWAY}/function/create-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    // Récupération des données retournées par votre backend
    serverMessage.value = data.message
    generatedPassword.value = data.password
    mfaSecret.value = data.mfa_secret
    
    // Conversion des QR codes base64 en images affichables
    passwordQrDisplay.value = `data:image/png;base64,${data.password_qr}`
    mfaQrDisplay.value = `data:image/png;base64,${data.mfa_qr}`
    
    accountCreated.value = true
    
  } catch (error) {
    console.error('Erreur lors de la création du compte:', error)
    errorMessage.value = 'Erreur lors de la création du compte. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Optionnel : afficher un message de confirmation
    console.log('Copied to clipboard:', text)
  })
}

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.qr-code-image {
  max-width: 200px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 10px auto;
}
</style>
