"""Inicializacion y versionado del esquema de la base de datos.

El esquema se versiona con PRAGMA user_version. Cada migracion es
idempotente para poder ejecutarse sobre bases de datos en cualquier
estado intermedio sin corromper datos.
"""
import logging

from . import createDB
from .createDB import (
    getConnection,
    createTable_PACIENTES, createTable_ANTECEDENTES, createTable_EXAMEN,
    createTable_ODONTOGRAMA, createTable_ODONTOGRAMA_DETAILS,
    createTable_TRATAMIENTO, migrateTRATAMIENTO_add_date, createTable_ABONO,
)

logger = logging.getLogger(__name__)

LATEST_SCHEMA_VERSION = 2


def _migration_1_baseline():
    """v1: tablas base del sistema."""
    createTable_PACIENTES()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
    createTable_TRATAMIENTO()
    createTable_ABONO()


MIGRATIONS = {
    1: _migration_1_baseline,
    2: migrateTRATAMIENTO_add_date,
}


def get_schema_version() -> int:
    conn = getConnection()
    try:
        return conn.execute("PRAGMA user_version").fetchone()[0]
    finally:
        conn.close()


def _set_schema_version(version: int):
    conn = getConnection()
    try:
        conn.execute(f"PRAGMA user_version = {int(version)}")
        conn.commit()
    finally:
        conn.close()


def run_migrations():
    current = get_schema_version()
    for version in range(current + 1, LATEST_SCHEMA_VERSION + 1):
        logger.info("Aplicando migracion de esquema v%s", version)
        MIGRATIONS[version]()
    if current < LATEST_SCHEMA_VERSION:
        _set_schema_version(LATEST_SCHEMA_VERSION)


def initialize_database():
    """Punto de entrada unico: migra datos legacy y aplica migraciones."""
    if createDB.migrate_legacy_db_if_needed():
        logger.info("Base de datos copiada desde la ubicacion anterior.")
    run_migrations()


if __name__ == "__main__":
    initialize_database()
