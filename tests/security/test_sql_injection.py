import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import createRow_PACIENTES, getConnection


class TestSQLInjection:
    MALICIOUS_INPUTS = [
        "SELECT * FROM pacientes",
        "INSERT INTO pacientes VALUES (1, 'hacker')",
        "DROP TABLE pacientes",
        "' OR 1=1 --",
        "'; DROP TABLE pacientes; --",
        "admin'--",
        "1' UNION SELECT * FROM usuarios--",
    ]

    def test_all_injection_payloads_stored_as_text(self, test_db):
        for payload in self.MALICIOUS_INPUTS:
            patient_id = createRow_PACIENTES(
                payload, "Perez", 30, "12345", "2024-01-15",
                "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas"
            )
            conn = getConnection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM pacientes WHERE patientID = ?", (patient_id,))
                row = cursor.fetchone()
                assert row[0] == payload
                cursor.execute("SELECT COUNT(*) FROM pacientes")
                assert cursor.fetchone()[0] >= 1
            finally:
                conn.close()

    def test_unicode_and_special_characters(self, test_db):
        payloads = [
            "Juan José Ñoño 日本語",
            "Juan @#$%^&*()_+{}|:<>?",
            "Juan\x00Perez",
        ]
        for payload in payloads:
            patient_id = createRow_PACIENTES(
                payload, "Perez", 30, "12345", "2024-01-15",
                "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas"
            )
            conn = getConnection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM pacientes WHERE patientID = ?", (patient_id,))
                assert cursor.fetchone()[0] == payload
            finally:
                conn.close()

    def test_extremely_long_strings(self, test_db):
        payload = "A" * 10000
        patient_id = createRow_PACIENTES(
            payload, "Perez", 30, "12345", "2024-01-15",
            "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas"
        )
        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM pacientes WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == payload
        finally:
            conn.close()
