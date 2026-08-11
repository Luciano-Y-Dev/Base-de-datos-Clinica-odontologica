import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import save_patient_atomic, getConnection


class TestAtomicSave:
    def test_atomic_save_all_data(self, test_db):
        antecedentes = [None] * 20
        examen = ["Normal", "TB", "TD", "Sano", "Normal"]

        patient_id = save_patient_atomic(
            None, "Juan", "Perez", 30, "12345", "2024-01-15",
            "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas",
            antecedentes, examen, None, None
        )
        assert patient_id is not None and patient_id > 0

        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM pacientes WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == "Juan"
        finally:
            conn.close()

    def test_atomic_save_rollback_on_error(self, test_db):
        antecedentes = [None] * 20
        examen = ["Normal", "TB", "TD", "Sano", "Normal"]

        with pytest.raises(Exception):
            save_patient_atomic(
                None, "", "Perez", 30, "12345", "2024-01-15",
                "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas",
                antecedentes, examen, None, None
            )

        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE name = ''")
            assert cursor.fetchone()[0] == 0
        finally:
            conn.close()

    def test_atomic_save_persists_all_tables(self, test_db):
        antecedentes = ["Oido", None, None, None, None, None, None, None, None, None,
                        None, None, None, None, "VIH Pos", None, None, None, None, None]
        examen = ["Normal", "TB", "TD", "Sano", "Normal"]
        odontogram = {"notes": "Notas", "affections": [
            {"tooth": 1, "face": "Oclusal", "affected": "Caries", "description": "Desc"}
        ]}
        abono = {"cost": 100.0, "amount": 50.0, "description": "Limpieza"}

        patient_id = save_patient_atomic(
            None, "Juan", "Perez", 30, "12345", "2024-01-15",
            "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas",
            antecedentes, examen, odontogram, abono
        )

        conn = getConnection()
        try:
            cursor = conn.cursor()
            for table in ["pacientes", "antecedentes_personales", "examen_fisico", "odontograms", "abonos"]:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE patientID = ?", (patient_id,))
                assert cursor.fetchone()[0] == 1, f"Missing row in {table}"
        finally:
            conn.close()
