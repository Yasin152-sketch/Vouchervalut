import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings


def get_cipher():
    # SECRET_KEY se secure 32-byte Fernet key derive karta hai
    key = base64.urlsafe_b64encode(
        hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    )
    return Fernet(key)


def encrypt_voucher_code(plain_code: str) -> str:
    cipher = get_cipher()
    return cipher.encrypt(plain_code.encode()).decode()


def decrypt_voucher_code(encrypted_text: str) -> str:
    cipher = get_cipher()
    return cipher.decrypt(encrypted_text.encode()).decode()
