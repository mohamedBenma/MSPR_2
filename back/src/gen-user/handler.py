import os
import json
import qrcode
import string
import secrets
import base64
from io import BytesIO
from cryptography.fernet import Fernet
from datetime import datetime
import psycopg2
import pyotp

def generate_password(length=24):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_qr_base64(data):
    """Génère un QR code en base64 à partir de données texte"""
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    return qr_base64

def handle(event, context):
    try:
        data = json.loads(event.body.decode("utf-8"))
        username = data.get("username", "").strip()
        if not username:
            return {
                "statusCode": 400,
                "body": "❌ Le champ 'username' est requis"
            }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": f"❌ Erreur parsing JSON : {str(e)}"
        }

    password = generate_password()
    mfa_secret = pyotp.random_base32()

    try:
        with open("/var/openfaas/secrets/fernet-key", "r") as f:
            FERNET_KEY = f.read().strip().encode()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"❌ Erreur lecture secret FERNET_KEY : {str(e)}"
        }

    cipher = Fernet(FERNET_KEY)
    encrypted_password = cipher.encrypt(password.encode()).decode()
    encrypted_mfa = cipher.encrypt(mfa_secret.encode()).decode()

    try:
        password_qr_b64 = generate_qr_base64(password)
        otp_uri = pyotp.totp.TOTP(mfa_secret).provisioning_uri(name=username, issuer_name="COFRAP")
        otp_qr_b64 = generate_qr_base64(otp_uri)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"❌ Erreur QR : {str(e)}"
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
        cur.execute("""
            INSERT INTO users (username, password, mfa_secret, gendate, expired)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (username, encrypted_password, encrypted_mfa, int(datetime.now().timestamp()), False))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": f"❌ Erreur BDD : {str(e)}"
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"✅ Utilisateur {username} créé avec succès",
            "username": username,
            "password": password,
            "password_qr": password_qr_b64,
            "mfa_secret": mfa_secret,
            "mfa_qr": otp_qr_b64
        })
    }
