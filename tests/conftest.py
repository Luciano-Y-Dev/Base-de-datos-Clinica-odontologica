import os
import sys
import tempfile
import sqlite3
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.crypto import _load_or_create_key, encrypt_field, decrypt_field
from database.createDB import (
    createTable_PACIENTES, createTable_ANTECEDENTES, createTable_EXAMEN,
    createTable_ODONTOGRAMA, createTable_ODONTOGRAMA_DETAILS, createTable_TRATAMIENTO, createTable_ABONO,
    createRow_PACIENTES, createRow_ANTECEDENTES, createRow_EXAMEN,
    createRow_ODONTOGRAMA, createRow_ODONTOGRAMA_DETAILS, createRow_ABONO,
    getConnection
)


@pytest.fixture
def test_db(tmp_path):
    """Create a fresh test database for each test."""
    import database.createDB as cdb_module
    original_db_path = cdb_module.DB_PATH
    test_db_path = str(tmp_path / "test_clinica.db")
    cdb_module.DB_PATH = test_db_path

    conn = sqlite3.connect(test_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.close()

    createTable_PACIENTES()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
    createTable_TRATAMIENTO()
    createTable_ABONO()

    yield test_db_path

    cdb_module.DB_PATH = original_db_path


@pytest.fixture
def sample_patient_data():
    """Return sample patient data for tests."""
    return {
        "name": "Juan",
        "lastName": "Perez",
        "age": 30,
        "CI": "12345678",
        "entryDate": "2024-01-15",
        "phoneNumber": "099123456",
        "home": "Av. Principal 123",
        "representName": "Maria Perez",
        "representCI": "87654321",
        "consultReason": "Dolor de muelas",
        "presentIssues": "Sangrado de encias",
    }


@pytest.fixture
def created_patient(test_db, sample_patient_data):
    """Create and return a patient ID for tests."""
    patient_id = createRow_PACIENTES(
        sample_patient_data["name"],
        sample_patient_data["lastName"],
        sample_patient_data["age"],
        sample_patient_data["CI"],
        sample_patient_data["entryDate"],
        sample_patient_data["phoneNumber"],
        sample_patient_data["home"],
        sample_patient_data["representName"],
        sample_patient_data["representCI"],
        sample_patient_data["consultReason"],
        sample_patient_data["presentIssues"],
    )
    return patient_id


@pytest.fixture
def sample_antecedentes_data():
    """Return sample antecedentes data."""
    return [
        "Dolor de oido", None, "Penicilina", None, None,
        None, None, None, None, None, None, None, None, None,
        "VIH Positivo", None, None, None, None, None
    ]


@pytest.fixture
def sample_examen_data():
    """Return sample examen data."""
    return ["Normal", "Sin hallazgos", "Sin hallazgos", "Sano", "Normal"]


@pytest.fixture
def sample_abono_data():
    """Return sample abono data."""
    return {
        "date": "2024-01-15",
        "description": "Limpieza dental",
        "treatmentCost": 100.0,
        "amount": 50.0,
        "remaining": 50.0,
    }
