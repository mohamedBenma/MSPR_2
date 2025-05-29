import os
import string
import secrets
import qrcode
import psycopg2
import pyotp
from flask import request
from cryptography.fernet import Fernet
from datetime import datetime

# 🔐 Lecture du secret sécurisé
try:
    with open("/var/openfaas/secrets/fernet-key", "r") as f:
        FERNET_KEY = f.read().strip().encode()
except Exception as e:
    FERNET_KEY = None

cipher = Fernet(FERNET_KEY)

def generate_password(length=24):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def handle():
    if not FERNET_KEY:
        return "❌ Clé FERNET absente."

    username = request.get_data(as_text=True).strip()

    try:
        conn = psycopg2.connect(
            dbname="usersDb",
            user="users",
            password="password",
            host="db",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT expired FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if not result:
            return "❌ Utilisateur introuvable."

        expired = result[0]
        if not expired:
            return "ℹ️ Le compte n'est pas expiré."

        new_password = generate_password()
        new_mfa_secret = pyotp.random_base32()

        encrypted_password = cipher.encrypt(new_password.encode()).decode()
        encrypted_mfa = cipher.encrypt(new_mfa_secret.encode()).decode()

        # QR Codes
        try:
            qr_pwd = qrcode.make(new_password)
            qr_pwd.save(f"/tmp/{username}_renew_pwd.png")

            otp_uri = pyotp.TOTP(new_mfa_secret).provisioning_uri(name=username, issuer_name="COFRAP")
            qr_2fa = qrcode.make(otp_uri)
            qr_2fa.save(f"/tmp/{username}_renew_2fa.png")
        except Exception as e:
            return f"❌ Erreur QR : {str(e)}"

        # Mise à jour BDD
        cur.execute("""
            UPDATE users
            SET password = %s,
                mfa_secret = %s,
                gendate = %s,
                expired = false
            WHERE username = %s
        """, (encrypted_password, encrypted_mfa, int(datetime.now().timestamp()), username))

        conn.commit()
        cur.close()
        conn.close()

        return f"✅ Nouveau mot de passe et 2FA générés pour {username}"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Erreur lors du renouvellement : {str(e)}"
