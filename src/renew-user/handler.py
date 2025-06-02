import os
import json
import string
import secrets
import qrcode
import psycopg2
import pyotp
import base64
from io import BytesIO
from cryptography.fernet import Fernet
from datetime import datetime

def generate_password(length=24):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_qr_base64(data):
    """Génère un QR code encodé en base64 à partir de texte"""
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def handle(event, context):
    try:
        username = event.body.decode("utf-8").strip()
        if not username:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "❌ Le champ 'username' est requis"})
            }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"❌ Erreur lecture de la requête : {str(e)}"})
        }

    try:
        with open("/var/openfaas/secrets/fernet-key", "r") as f:
            FERNET_KEY = f.read().strip().encode()
        cipher = Fernet(FERNET_KEY)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"❌ Clé FERNET introuvable : {str(e)}"})
        }

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
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "❌ Utilisateur introuvable."})
            }

        expired = result[0]
        if not expired:
            return {
                "statusCode": 200,
                "body": json.dumps({"info": "ℹ️ Le compte n'est pas expiré."})
            }

        # Génération des nouveaux identifiants
        new_password = generate_password()
        new_mfa_secret = pyotp.random_base32()

        encrypted_password = cipher.encrypt(new_password.encode()).decode()
        encrypted_mfa = cipher.encrypt(new_mfa_secret.encode()).decode()

        # QR Codes en base64
        password_qr_b64 = generate_qr_base64(new_password)
        otp_uri = pyotp.TOTP(new_mfa_secret).provisioning_uri(name=username, issuer_name="COFRAP")
        otp_qr_b64 = generate_qr_base64(otp_uri)

        # Mise à jour en BDD
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

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"✅ Nouveau mot de passe et MFA régénérés pour {username}",
                "username": username,
                "password": new_password,
                "password_qr": password_qr_b64,
                "mfa_secret": new_mfa_secret,
                "mfa_qr": otp_qr_b64
            })
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"❌ Erreur lors du renouvellement : {str(e)}"})
        }
