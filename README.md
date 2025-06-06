# MSPR_2

### Backend

# 🐳 Déploiement OpenFaaS avec PostgreSQL et Adminer

## 📁 Prérequis

- Docker
- `k3d`, `kubectl`, `helm`, `faas-cli`
- Fichier `init.sql` (script d'init de la base)
- Fichier `stack.yml` (configuration des fonctions)

---

## ⚙️ Étapes de déploiement

### 1. Créer le cluster K3D

```bash
k3d cluster create openfaas \
  --agents 2 \
  -p "31112:8080@loadbalancer" \
  --registry-create k3d-registry.local
```

### 2. Ajouter le repo Helm et installer OpenFaaS

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update

helm upgrade openfaas openfaas/openfaas \
  --namespace openfaas \
  --create-namespace \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true \
  --set serviceType=NodePort \
  --set gateway.nodePort=31112 \
  --install
```

### 3. Récupérer le mot de passe admin et se connecter

```bash
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
faas-cli login --username admin --password $PASSWORD --gateway http://127.0.0.1:31112
```

### 4. Rediriger le port du gateway en local

```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

---

## 🗃 Déploiement PostgreSQL, Adminer et init

### 5. Déployer PostgreSQL et Adminer

```bash
kubectl apply -f db-deploy.yaml
kubectl apply -f deploy-adminer.yaml
```

### 6. Créer le ConfigMap pour le script SQL

```bash
kubectl create configmap init-sql \
  --from-file=init.sql \
  -n openfaas-fn
```

### 7. Lancer le Job d'initialisation de la base

```bash
kubectl apply -f job-init.yaml

# Vérifier que le job a bien fonctionné :
kubectl logs job/init-db -n openfaas-fn
```

---

## 🚀 Build, push & deploy des fonctions

### 8. Utiliser `faas-cli` pour déployer

#### S'authentifier au package GHRC :

```bash
  echo "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" | docker login ghcr.io -u $PseudoGithub --password-stdin
```

```bash
faas-cli up -f stack.yml --gateway http://127.0.0.1:8080
```

---

## 🧪 Tester les fonctions

```bash
# Générer un utilisateur
echo '{"username": "mohamed"}' | faas-cli invoke gen-user --gateway http://127.0.0.1:8080

# Authentifier un utilisateur
echo '{"username": "mohamed", "password": "le_mdp", "code": "123456"}' | faas-cli invoke auth-user --gateway http://127.0.0.1:8080

# Renouveler un secret
echo '{"username": "mohamed"}' | faas-cli invoke renew-user --gateway http://127.0.0.1:8080
```

---

## 🖥 Interface Web OpenFaaS

Accéder via navigateur :

👉 [http://127.0.0.1:8080](http://127.0.0.1:8080)

Login : `admin`  
Mot de passe : `$PASSWORD` (voir étape 3)
