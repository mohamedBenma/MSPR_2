<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card class="pa-8" elevation="8" rounded="xl">
          <!-- Logo -->
          <div class="text-center mb-2">
            <v-img
              src="@/assets/logo.png"
              alt="Logo"
              width="140"
              class="mx-auto mb-2"
            />
          </div>
          <!-- Titre -->
          <div class="text-center mb-6">
            <h2 class="font-weight-bold mb-1">Renew your credentials</h2>
          </div>

          <!-- Formulaire -->
          <v-form
            @submit.prevent="renewCredentials"
            ref="form"
            v-model="formValid"
          >
            <v-text-field
              v-model="username"
              label="Username"
              prepend-inner-icon="mdi-account"
              :rules="[(v) => !!v || 'Username is required']"
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
              color="warning"
              type="submit"
              block
              large
              :loading="loading"
              :disabled="!formValid || loading"
              class="mb-2"
            >
              Renew Credentials
            </v-btn>
          </v-form>

          <!-- Section QR Codes renouvelés -->
          <v-expand-transition>
            <div v-if="credentialsRenewed" class="mt-6">
              <v-alert type="success" class="mb-4">
                {{ serverMessage }}
              </v-alert>

              <!-- Nouveau mot de passe -->
              <v-card outlined class="mb-4 pa-4">
                <h3 class="mb-3">🔐 New Password</h3>
                <v-text-field
                  :value="newPassword"
                  label="New Password"
                  readonly
                  outlined
                  dense
                  append-icon="mdi-content-copy"
                  @click:append="copyToClipboard(newPassword)"
                />

                <!-- QR Code du nouveau mot de passe -->
                <div class="text-center mb-3">
                  <p class="text-body-2 mb-2">
                    Scan this QR code for your new password:
                  </p>
                  <img
                    :src="newPasswordQrDisplay"
                    alt="New Password QR Code"
                    class="qr-code-image"
                  />
                </div>
              </v-card>

              <!-- Nouveau secret 2FA -->
              <v-card outlined class="mb-4 pa-4">
                <h3 class="mb-3">📱 New 2FA Secret</h3>
                <v-text-field
                  :value="newMfaSecret"
                  label="New 2FA Secret"
                  readonly
                  outlined
                  dense
                  append-icon="mdi-content-copy"
                  @click:append="copyToClipboard(newMfaSecret)"
                />

                <!-- QR Code 2FA -->
                <div class="text-center mb-3">
                  <p class="text-body-2 mb-2">
                    Scan this QR code with your authenticator app:
                  </p>
                  <img
                    :src="newMfaQrDisplay"
                    alt="New 2FA QR Code"
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
                Go to Login with new credentials
              </v-btn>
            </div>
          </v-expand-transition>

          <!-- Lien vers connexion -->
          <div class="text-center mt-4">
            <span
              >Remember your credentials?
              <v-btn
                variant="text"
                color="primary"
                class="pa-0"
                @click="goToLogin"
              >
                Back to Login
              </v-btn>
            </span>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const loading = ref(false);
const formValid = ref(false);
const errorMessage = ref("");
const credentialsRenewed = ref(false);
const serverMessage = ref("");
const newPassword = ref("");
const newMfaSecret = ref("");
const newPasswordQrDisplay = ref("");
const newMfaQrDisplay = ref("");

// URL de votre gateway OpenFaaS
//const OPENFAAS_GATEWAY = 'http://127.0.0.1:8080'

async function renewCredentials() {
  errorMessage.value = "";
  loading.value = true;

  try {
    // Appel à votre fonction OpenFaaS de renouvellement
    const response = await fetch("/function/renew-user", {
      method: "POST",
      headers: {
        "Content-Type": "text/plain",
      },
      body: username.value,
    });

    const data = await response.json();

    if (response.status === 200 && data.message) {
      // Succès du renouvellement
      serverMessage.value = data.message;
      newPassword.value = data.password;
      newMfaSecret.value = data.mfa_secret;

      // Conversion des QR codes base64 en images affichables
      newPasswordQrDisplay.value = `data:image/png;base64,${data.password_qr}`;
      newMfaQrDisplay.value = `data:image/png;base64,${data.mfa_qr}`;

      credentialsRenewed.value = true;
    } else if (response.status === 404) {
      errorMessage.value = data.error;
    } else if (response.status === 200 && data.info) {
      errorMessage.value = data.info;
    } else {
      errorMessage.value = data.error || "Erreur lors du renouvellement";
    }
  } catch (error) {
    console.error("Erreur lors du renouvellement:", error);
    errorMessage.value = "Erreur de connexion au serveur. Veuillez réessayer.";
  } finally {
    loading.value = false;
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    console.log("Copied to clipboard:", text);
  });
}

function goToLogin() {
  router.push("/login");
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
