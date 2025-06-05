<template>
  <v-app>
    <!-- HEADER -->
    <v-app-bar color="white" flat>
      <v-row align="center" class="flex-grow-1">
        <v-col cols="auto" style="width: 200px;">
          <v-img
            :src="lacofrapLogo"
            alt="Logo"
            width="150"
            class="logo-img"
          />
        </v-col>
        <v-col>
          <span class="font-weight-bold text-h6"></span>
        </v-col>
        <v-col cols="auto">
          <v-btn color="primary" class="mr-2" @click="goToLogin">Log in</v-btn>
          <v-btn color="primary" outlined @click="goToRegister">Register</v-btn>
        </v-col>
      </v-row>
    </v-app-bar>

    <!-- MAIN CONTENT -->
    <v-main>
      <v-container>
        <!-- Fil d'Ariane -->
        <div class="text-caption mb-2 grey--text">
         
        </div>

        <!-- Titre principal -->
        <h1 class="display-1 font-weight-bold mb-4">Services COFRAP</h1>

        <!-- Sous-titre -->
        <div class="mb-6 text-subtitle-1">
          Découvrez comment la sécurité et l'innovation s’allient pour améliorer la gestion de vos accès et la protection de vos données.
        </div>

        <!-- Grille principale -->
        <v-row>
          <v-col cols="12" md="7">
            <div class="mb-4">
              <div class="text-h6 mb-2">Pourquoi choisir notre solution ?</div>
              <ul>
                <li>Sécurité renforcée : mots de passe complexes et authentification 2FA obligatoire.</li>
                <li>Gestion automatisée des renouvellements d’identifiants.</li>
                <li>Interface simple, accessible et inclusive.</li>
                <li>Déploiement rapide grâce aux technologies serverless.</li>
              </ul>
            </div>
            <v-row>
              <v-col cols="12" sm="6">
                <v-btn color="primary" block class="mb-2">Lire l’étude de cas</v-btn>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn color="primary" outlined block>Prendre rendez-vous</v-btn>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" md="5">
            <!-- Mosaïque d’images -->
            <v-row dense>
              <v-col cols="6">
                <v-img src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80" aspect-ratio="1" class="rounded-lg mb-2" />
              </v-col>
              <v-col cols="6">
                <v-img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80" aspect-ratio="1" class="rounded-lg mb-2" />
              </v-col>
              <v-col cols="12">
                <v-img src="https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=800&q=80" aspect-ratio="2.5" class="rounded-lg" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'
import lacofrapLogo from '../assets/lacofrap.png' // <-- IMPORT correct

const router = useRouter()

function goToLogin() {
  router.push('/login')
}
function goToRegister() {
  router.push('/register')
}
</script>

<style scoped>
ul {
  padding-left: 1.2em;
  margin-bottom: 1.5em;
}
li {
  margin-bottom: 0.5em;
  font-size: 1.1rem;
}
.logo-img {
  background-color: #f0f0f0; /* Pour voir l'image si elle est blanche */
  border-radius: 8px;
}
</style>
