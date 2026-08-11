"""Respaldos de la base de datos y la clave de cifrado.

- Respaldo automatico rotativo (carpeta Backups del perfil del usuario).
- Respaldo manual a una carpeta elegida por la usuaria (ej. USB).
- Restauracion desde una carpeta de respaldo.

Cada respaldo es una carpeta "respaldo_<fecha>" que contiene Clinica.db y
secret.key (sin la clave, los campos cifrados serian irrecuperables).
"""
from __future__ import annotations

import logging
import os
import shutil
from datetime import datetime

import platformdirs

from database import createDB, crypto

logger = logging.getLogger(__name__)

_APP_NAME = "clinica_odontologica"
BACKUP_DIR = os.path.join(platformdirs.user_data_dir(_APP_NAME, appauthor=False), "Backups")
MAX_BACKUPS = 10

_DB_FILE = "Clinica.db"
_KEY_FILE = "secret.key"


def _copy_backup_files(dest_dir: str) -> None:
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(createDB.DB_PATH):
        shutil.copy2(createDB.DB_PATH, os.path.join(dest_dir, _DB_FILE))
    else:
        raise FileNotFoundError("No se encontro la base de datos para respaldar.")
    if os.path.exists(crypto.KEY_PATH):
        shutil.copy2(crypto.KEY_PATH, os.path.join(dest_dir, _KEY_FILE))


def create_backup(dest_root: str | None = None) -> str:
    """Crea un respaldo. Sin dest_root usa la carpeta automatica (con rotacion).
    Devuelve la ruta de la carpeta de respaldo creada."""
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    root = dest_root if dest_root else BACKUP_DIR
    dest = os.path.join(root, f"respaldo_{stamp}")
    _copy_backup_files(dest)
    logger.info("Respaldo creado en %s", dest)
    if dest_root is None:
        _rotate()
    return dest


def _rotate() -> None:
    try:
        backups = sorted(
            d for d in os.listdir(BACKUP_DIR)
            if d.startswith("respaldo_") and os.path.isdir(os.path.join(BACKUP_DIR, d))
        )
    except FileNotFoundError:
        return
    while len(backups) > MAX_BACKUPS:
        oldest = backups.pop(0)
        shutil.rmtree(os.path.join(BACKUP_DIR, oldest), ignore_errors=True)
        logger.info("Respaldo antiguo eliminado: %s", oldest)


def auto_backup() -> str | None:
    """Respaldo automatico silencioso (al cerrar la app). Nunca lanza errores."""
    try:
        return create_backup()
    except Exception:
        logger.exception("Fallo el respaldo automatico")
        return None


def restore_backup(backup_dir: str) -> None:
    """Reemplaza la base de datos y la clave actuales por las del respaldo."""
    db_src = os.path.join(backup_dir, _DB_FILE)
    if not os.path.exists(db_src):
        raise FileNotFoundError(
            "La carpeta seleccionada no contiene un respaldo valido (falta Clinica.db)."
        )

    # Respaldo de seguridad del estado actual antes de sobrescribir
    try:
        create_backup()
    except Exception:
        logger.exception("No se pudo crear el respaldo previo a la restauracion")

    os.makedirs(os.path.dirname(createDB.DB_PATH), exist_ok=True)
    shutil.copy2(db_src, createDB.DB_PATH)

    key_src = os.path.join(backup_dir, _KEY_FILE)
    if os.path.exists(key_src):
        os.makedirs(os.path.dirname(crypto.KEY_PATH), exist_ok=True)
        shutil.copy2(key_src, crypto.KEY_PATH)
    crypto.reload_key()
    logger.info("Respaldo restaurado desde %s", backup_dir)
