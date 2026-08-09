import os
import base64
from cryptography.fernet import Fernet

KEY_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secret.key")


def _load_or_create_key() -> bytes:
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key


_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(_load_or_create_key())
    return _fernet


def encrypt_field(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    f = _get_fernet()
    encrypted = f.encrypt(str(value).encode("utf-8"))
    return base64.urlsafe_b64encode(encrypted).decode("utf-8")


def decrypt_field(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    f = _get_fernet()
    try:
        encrypted = base64.urlsafe_b64decode(value.encode("utf-8"))
        return f.decrypt(encrypted).decode("utf-8")
    except Exception:
        return value


SENSITIVE_FIELDS_PACIENTES = {
    "CI": 4,
    "representCI": 9,
}

SENSITIVE_FIELDS_ANTECEDENTES = {
    "hiv": 16,
}
