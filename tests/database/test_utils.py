import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import createRow_PACIENTES, createRow_ABONO
from database.utils import (
    readPACIENTE, readREMAINING, readTable_PACIENTES_ordered,
    readPATIENTS_with_remaining_all
)


class TestReadPatientOrdered:
    def test_ordered_by_date_desc(self, test_db, sample_patient_data):
        createRow_PACIENTES(
            sample_patient_data["name"],
            sample_patient_data["lastName"],
            sample_patient_data["age"],
            sample_patient_data["CI"],
            "2024-01-01",
            sample_patient_data["phoneNumber"],
            sample_patient_data["home"],
            sample_patient_data["representName"],
            sample_patient_data["representCI"],
            sample_patient_data["consultReason"],
            sample_patient_data["presentIssues"],
        )
        patients = readTable_PACIENTES_ordered()
        assert len(patients) >= 1


class TestReadWithRemaining:
    def test_read_with_remaining_balance(self, test_db, sample_patient_data):
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
        createRow_ABONO(patient_id, "2024-01-01", "Limpieza", 100.0, 50.0, 50.0)
        remaining = readREMAINING(patient_id)
        assert remaining == 50.0
