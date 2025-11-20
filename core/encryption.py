import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class PasswordManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.enc_file = os.path.join("data", "saved_passwords.enc")
        self.salt_file = os.path.join("data", "salt.bin")

    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def save_password(self, password: str, master_password: str):
        saved = self.load_passwords(master_password) or []
        saved.append({"password": password, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return self._encrypt_and_save(saved, master_password)

    def load_passwords(self, master_password: str):
        if not os.path.exists(self.enc_file):
            return []

        if not os.path.exists(self.salt_file):
            return None

        with open(self.salt_file, "rb") as f:
            salt = f.read()

        try:
            key = self.derive_key(master_password, salt)
            fernet = Fernet(key)
            with open(self.enc_file, "rb") as f:
                data = fernet.decrypt(f.read())
            return json.loads(data.decode())
        except Exception:
            return None

    def _encrypt_and_save(self, data, master_password):
        try:
            salt = os.urandom(16) if not os.path.exists(self.salt_file) else open(self.salt_file, "rb").read()
            if not os.path.exists(self.salt_file):
                with open(self.salt_file, "wb") as f:
                    f.write(salt)

            key = self.derive_key(master_password, salt)
            fernet = Fernet(key)
            encrypted = fernet.encrypt(json.dumps(data, ensure_ascii=False, indent=4).encode())

            with open(self.enc_file, "wb") as f:
                f.write(encrypted)
            return True
        except Exception:
            return False
