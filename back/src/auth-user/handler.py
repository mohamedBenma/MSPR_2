import json
import psycopg2
import pyotp
from cryptography.fernet import Fernet

def handle(event, context):
    try:
        data = json.loads(event.body.decode("utf-8"))
        username = data.get("username", "").strip()
        password_attempt = data.get("password", "").strip()
        code_attempt = data.get("code", "").strip()

        if not all([username, password_attempt, code_attempt]):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "❌ Requête incomplète. Champs requis : username, password, code."
                })
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"❌ Erreur parsing JSON : {str(e)}"
            })
        }

    try:
        with open("/var/openfaas/secrets/fernet-key", "r") as f:
            FERNET_KEY = f.read().strip().encode()
        cipher = Fernet(FERNET_KEY)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"❌ Clé FERNET introuvable ou invalide : {str(e)}"
            })
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
        cur.execute("SELECT password, mfa_secret, expired FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "error": "❌ Utilisateur introuvable."
                })
            }

        encrypted_password, encrypted_mfa, expired = result

        if expired:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "error": "❌ Identifiants expirés. Veuillez régénérer un compte."
                })
            }

        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        decrypted_mfa = cipher.decrypt(encrypted_mfa.encode()).decode()

        if password_attempt != decrypted_password:
            return {
                "statusCode": 401,
                "body": json.dumps({
                    "error": "❌ Mot de passe incorrect."
                })
            }

        totp = pyotp.TOTP(decrypted_mfa)
        if not totp.verify(code_attempt):
            return {
                "statusCode": 401,
                "body": json.dumps({
                    "error": "❌ Code 2FA invalide ou expiré."
                })
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "✅ Authentification réussie !",
                "username": username
            })
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"❌ Erreur interne : {str(e)}"
            })
        }
