import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import createRow_PACIENTES, createRow_ANTECEDENTES, getConnection


class TestDataProtection:
    def test_ci_encrypted_in_database(self, test_db, sample_patient_data):
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
        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT CI, representCI FROM pacientes WHERE patientID = ?", (patient_id,))
            row = cursor.fetchone()
            assert row[0] != sample_patient_data["CI"]
            assert row[1] != sample_patient_data["representCI"]
        finally:
            conn.close()

    def test_hiv_encrypted_in_database(self, test_db, created_patient):
        antecedentes = [None] * 20
        antecedentes[14] = "VIH Positivo"
        createRow_ANTECEDENTES(created_patient, *antecedentes)
        conn = getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT hiv FROM antecedentes_personales WHERE patientID = ?", (created_patient,))
            row = cursor.fetchone()
            assert row[0] != "VIH Positivo"
        finally:
            conn.close()

    def test_sensitive_data_decrypted_on_read(self, test_db, sample_patient_data):
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
        from database.utils import readPACIENTE
        patient = readPACIENTE(patient_id)
        assert patient.CI == sample_patient_data["CI"]
        assert patient.representCI == sample_patient_data["representCI"]
