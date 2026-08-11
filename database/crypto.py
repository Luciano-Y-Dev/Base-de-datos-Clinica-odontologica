import os
import base64
import logging
import platformdirs
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

_APP_NAME = "clinica_odontologica"
_KEY_DIR = platformdirs.user_config_dir(_APP_NAME, appauthor=False)
KEY_PATH = os.path.join(_KEY_DIR, "secret.key")
_LEGACY_KEY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "secret.key"
)


def _load_or_create_key() -> bytes:
    if os.path.exists(_LEGACY_KEY_PATH) and not os.path.exists(KEY_PATH):
        os.makedirs(_KEY_DIR, exist_ok=True)
        os.rename(_LEGACY_KEY_PATH, KEY_PATH)

    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            return f.read()

    key = Fernet.generate_key()
    os.makedirs(_KEY_DIR, exist_ok=True)
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


def reload_key() -> None:
    """Descarta la clave en memoria (usar tras restaurar un respaldo)."""
    global _fernet
    _fernet = None


def _looks_like_fernet_token(value: str) -> bool:
    """Detecta si un valor tiene estructura de token Fernet (aunque no se
    pueda descifrar con la clave actual). La app envuelve el token en una
    segunda capa de base64, por eso se revisan ambas capas."""
    try:
        raw = base64.urlsafe_b64decode(value.encode("utf-8"))
        if len(raw) >= 73 and raw[0] == 0x80:
            return True
        raw2 = base64.urlsafe_b64decode(raw)
        return len(raw2) >= 73 and raw2[0] == 0x80
    except Exception:
        return False


def decrypt_field(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    f = _get_fernet()
    try:
        encrypted = base64.urlsafe_b64decode(value.encode("utf-8"))
        return f.decrypt(encrypted).decode("utf-8")
    except Exception:
        if _looks_like_fernet_token(value):
            # Cifrado con otra clave (clave perdida/cambiada): NO devolver el
            # token en crudo, porque si se vuelve a guardar se re-cifraria y
            # el dato quedaria irrecuperable incluso recuperando la clave.
            logger.warning("Campo cifrado ilegible (clave distinta o perdida)")
            return ""
        # Dato legacy en texto plano (anterior al cifrado): se muestra tal cual.
        return value


SENSITIVE_FIELDS_PACIENTES = {
    "CI": 4,
    "representCI": 9,
}

SENSITIVE_FIELDS_ANTECEDENTES = {
    "hiv": 16,
}
