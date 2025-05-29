import os
import qrcode
import string
import secrets
from cryptography.fernet import Fernet
from datetime import datetime
import psycopg2
import pyotp

def generate_password(length=24):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def handle(req):
    username = req.strip()
    password = generate_password()
    mfa_secret = pyotp.random_base32()

    # 🔐 Lecture sécurisée de la clé via OpenFaaS secret
    try:
        with open("/var/openfaas/secrets/fernet-key", "r") as f:
            FERNET_KEY = f.read().strip().encode()
    except Exception as e:
        return f"❌ Erreur lecture secret FERNET_KEY : {str(e)}"

    cipher = Fernet(FERNET_KEY)
    encrypted_password = cipher.encrypt(password.encode()).decode()
    encrypted_mfa = cipher.encrypt(mfa_secret.encode()).decode()

    # QR Code
    try:
        qr_path = f"/tmp/{username}_password_qr.png"
        qrcode.make(password).save(qr_path)

        otp_uri = pyotp.totp.TOTP(mfa_secret).provisioning_uri(name=username, issuer_name="COFRAP")
        otp_qr_path = f"/tmp/{username}_2fa_qr.png"
        qrcode.make(otp_uri).save(otp_qr_path)
    except Exception as e:
        return f"❌ Erreur QR : {str(e)}"

    # Connexion BDD
    try:
        conn = psycopg2.connect(
            dbname="usersDb",
            user="users",
            password="password",
            host="db",  # "localhost" si tu testes hors conteneur
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
        return f"❌ Erreur BDD : {str(e)}"

    return f"✅ Utilisateur {username} créé avec succès"
