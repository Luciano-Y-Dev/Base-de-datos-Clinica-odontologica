import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import (
    createRow_PACIENTES, readTable_PACIENTES, updateRow_PACIENTES,
    deleteRow_PACIENTES, createRow_ANTECEDENTES, createRow_ABONO,
    getConnection
)


class TestPacienteCRUD:
    def test_create_and_read_paciente(self, test_db, sample_patient_data):
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
        assert patient_id is not None and patient_id > 0
        pacientes = readTable_PACIENTES()
        assert len(pacientes) >= 1

    def test_update_paciente(self, test_db, sample_patient_data):
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
        updateRow_PACIENTES(
            patient_id, "Juan Actualizado", "Perez", 31, "12345",
            "2024-01-15", "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas"
        )
        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM pacientes WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == "Juan Actualizado"
        finally:
            conn.close()

    def test_delete_cascade(self, test_db, sample_patient_data):
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
        createRow_ANTECEDENTES(
            patient_id, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None
        )
        createRow_ABONO(patient_id, "2024-01-01", "Limpieza", 100.0, 50.0, 50.0)
        deleteRow_PACIENTES(patient_id)
        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == 0
            cursor.execute("SELECT COUNT(*) FROM antecedentes_personales WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == 0
            cursor.execute("SELECT COUNT(*) FROM abonos WHERE patientID = ?", (patient_id,))
            assert cursor.fetchone()[0] == 0
        finally:
            conn.close()
