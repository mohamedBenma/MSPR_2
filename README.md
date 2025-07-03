# COFRAP_Project_Documentation

### Backend & Frontend

# 🐳 Déploiement OpenFaaS avec PostgreSQL, Adminer et Interface Web locale

## 📁 Prérequis

- Docker
- `k3d`, `kubectl`, `helm`, `faas-cli`
- Fichier `init.sql` (script d'init de la base)
- Fichier `stack.yml` (configuration des fonctions)
- Fichier `fernet-key` (clé de chiffrement générée via Python)
- Accès à un compte GitHub pour l'hébergement des images Docker via GHCR

---

## ⚙️ Étapes de déploiement

### 1. Créer le cluster K3D

```bash
k3d cluster create openfaas   --agents 2   -p "31112:8080@loadbalancer"   --registry-create k3d-registry.local
```

### 2. Ajouter le repo Helm et installer OpenFaaS

#### Créer les namespaces nécessaires :

```bash
kubectl create ns openfaas-fn
kubectl create ns openfaas
```

#### Ajouter le repo et installer OpenFaaS avec Helm :

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update

helm upgrade openfaas openfaas/openfaas   --namespace openfaas   --create-namespace   --set functionNamespace=openfaas-fn   --set generateBasicAuth=true   --set serviceType=NodePort   --set gateway.nodePort=31112   --install
```

### 3. Récupérer le mot de passe admin et se connecter

```bash
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
faas-cli login --username admin --password $PASSWORD --gateway http://127.0.0.1:31112
```

### 4. Rediriger le port du gateway en local (optionnel pour test frontend)

```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

---

## 🗃 Déploiement PostgreSQL, Adminer et initialisation

### 5. Déployer PostgreSQL et Adminer

```bash
kubectl apply -f db-deploy.yaml
kubectl apply -f deploy-adminer.yaml
```

### 6. Créer le ConfigMap pour le script SQL

```bash
kubectl create configmap init-sql   --from-file=init.sql   -n openfaas-fn
```

### 7. Créer le secret Fernet (clé de chiffrement)

```bash
kubectl create secret generic fernet-key   --from-literal=fernet-key=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")   -n openfaas-fn
```

### 8. Lancer le Job d'initialisation de la base

```bash
kubectl apply -f job-init.yaml

# Vérifier que le job a bien fonctionné :
kubectl logs job/init-db -n openfaas-fn
```

---

## 🚀 Build, push & deploy des fonctions

### 9. S'authentifier auprès de GHCR (GitHub Container Registry)

```bash
echo "<TOKEN_PERSONNEL>" | docker login ghcr.io -u <PseudoGithub> --password-stdin
```

### 10. Déployer les fonctions via `stack.yml`

```bash
faas-cli up -f stack.yml --gateway http://127.0.0.1:31112
```

---

## 🧪 Tester les fonctions (via CLI)

```bash
# Générer un utilisateur
echo '{"username": "badr"}' | faas-cli invoke gen-user --gateway http://127.0.0.1:8080

# Authentifier un utilisateur
echo '{"username": "mohamed", "password": "le_mdp", "code": "123456"}' | faas-cli invoke auth-user --gateway http://127.0.0.1:8080

# Renouveler un secret
echo '{"username": "mohamed"}' | faas-cli invoke renew-user --gateway http://127.0.0.1:8080
```

### Visualisation PostgreSQL via Adminer

```bash
kubectl port-forward -n openfaas-fn svc/adminer 8082:8080
```

Ouvrir dans le navigateur : [http://localhost:8082](http://localhost:8082)

---

## 🖥 Interface Web OpenFaaS

Accéder via navigateur :
👉 [http://127.0.0.1:8080](http://127.0.0.1:8080)

Login : `admin`  
Mot de passe : `$PASSWORD` (voir étape 3)

---

## 💻 Interface Frontend (test local)

### 1. Lancer le frontend en local (ex. avec Node.js)

Depuis le dossier `/front` :

```bash
npm install
npm run dev
```

L’interface est disponible sur [http://localhost:3000](http://localhost:3000)

### 2. Tester les parcours utilisateurs

- Génération de QR code pour MFA
- Authentification 2FA avec mot de passe + TOTP
- Renouvellement de compte expiré

L’interface utilise les endpoints exposés par OpenFaaS pour interagir avec les fonctions via HTTP.

---

## 📌 Conseils & Rappels

- 🔐 Vérifier que le secret `fernet-key` est bien monté pour toutes les fonctions.
- 🧪 Tester d’abord avec `faas-cli`, puis via l’interface web.
- 🔁 Se reconnecter avec `faas-cli login` après chaque redémarrage du cluster.
- 🛠 En cas de modification du code Python, rebuild des images et mise à jour du `stack.yml` nécessaires.

---

🧩 Projet intégralement containerisé, déployé en local avec K3s, compatible cloud-native et sécurisé par chiffrement Fernet + MFA.
