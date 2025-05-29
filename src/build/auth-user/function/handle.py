import os
import json
import psycopg2
import pyotp
from flask import request
from cryptography.fernet import Fernet

# 🔐 Lecture du secret depuis le chemin OpenFaaS
try:
    with open("/var/openfaas/secrets/fernet-key", "r") as f:
        FERNET_KEY = f.read().strip().encode()
except Exception as e:
    FERNET_KEY = None

cipher = Fernet(FERNET_KEY)

def handle():
    if not FERNET_KEY:
        return "❌ Clé FERNET introuvable."

    try:
        data = request.get_json()
        username = data.get("username")
        password_attempt = data.get("password")
        code_attempt = data.get("code")

        if not all([username, password_attempt, code_attempt]):
            return "❌ Requête incomplète. Champs requis : username, password, code."

        # Connexion BDD
        conn = psycopg2.connect(
            dbname="usersDb",
            user="users",
            password="password",
            host="db",  # ou "localhost" hors conteneur
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT password, mfa_secret, expired FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            return "❌ Utilisateur introuvable."

        encrypted_password, encrypted_mfa, expired = result

        if expired:
            return "❌ Identifiants expirés. Veuillez régénérer un compte."

        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        decrypted_mfa = cipher.decrypt(encrypted_mfa.encode()).decode()

        if password_attempt != decrypted_password:
            return "❌ Mot de passe incorrect."

        totp = pyotp.TOTP(decrypted_mfa)
        if not totp.verify(code_attempt):
            return "❌ Code 2FA invalide ou expiré."

        return "✅ Authentification réussie !"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Erreur d'authentification : {str(e)}"
