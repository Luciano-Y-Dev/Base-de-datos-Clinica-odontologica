import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.patient_service import (
    _validate_required, delete_patient, get_patient, filter_patients, ci_exists
)
from database.models import Paciente


class TestValidation:
    def test_validate_required_empty_raises(self):
        with pytest.raises(ValueError, match="obligatorio"):
            _validate_required("", "Nombre")

    def test_validate_required_none_raises(self):
        with pytest.raises(ValueError, match="obligatorio"):
            _validate_required(None, "Apellido")


class TestDeletePatient:
    def test_delete_patient_success(self, test_db, created_patient):
        result = delete_patient(created_patient)
        assert result is True

    def test_delete_nonexistent_patient(self, test_db):
        result = delete_patient(999999)
        assert result is True


class TestGetPatient:
    def test_get_patient_by_id(self, test_db, created_patient):
        patient = get_patient(created_patient)
        assert patient is not None
        assert patient.name == "Juan"

    def test_get_patient_returns_none_for_missing(self, test_db):
        patient = get_patient(999999)
        assert patient is None


class TestFilterPatients:
    def test_filter_by_name(self, test_db, created_patient):
        from database.utils import readTable_PACIENTES_ordered
        patients = readTable_PACIENTES_ordered()
        result = filter_patients(patients, "Juan")
        assert len(result) >= 1
        assert result[0].name == "Juan"

    def test_filter_by_nonexistent_name(self, test_db, created_patient):
        from database.utils import readTable_PACIENTES_ordered
        patients = readTable_PACIENTES_ordered()
        result = filter_patients(patients, "ZZZZ")
        assert len(result) == 0


class TestCiExists:
    def test_ci_exists_true_for_existing(self, test_db, created_patient):
        assert ci_exists("12345678") is True

    def test_ci_exists_false_for_new(self, test_db, created_patient):
        assert ci_exists("99999999") is False

    def test_ci_exists_excludes_same_patient(self, test_db, created_patient):
        assert ci_exists("12345678", exclude_patient_id=created_patient) is False
