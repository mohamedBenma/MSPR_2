import os
import qrcode
import string
import secrets
from cryptography.fernet import Fernet
from datetime import datetime
import psycopg2

def generate_password(length=24):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

print (generate_password(14))

def handle(username):
    password = generate_password()
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    print("password: ",password)
    # Génération du QR Code
    qr = qrcode.make(password)
    qr_path = f"{username}_password_qr.png"
    qr.save(qr_path)

    # Enregistrement en BDD
    conn = psycopg2.connect(
        dbname="yourdb", user="user", password="pass", host="db"
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, gendate, expired) VALUES (%s, %s, %s, %s)",
                (username, encrypted_password, int(datetime.now().timestamp()), 0))
    conn.commit()
    cur.close()
    conn.close()

    return f"Mot de passe généré pour {username} + QR enregistré"
handle('mohamed')
