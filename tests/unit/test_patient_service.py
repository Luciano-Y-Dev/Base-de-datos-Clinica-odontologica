import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.patient_service import (
    _validate_required, _validate_int, _validate_float,
    delete_patient, get_patient, filter_patients
)
from database.models import Paciente


class TestValidation:
    def test_validate_required_success(self):
        assert _validate_required("Juan", "Nombre") is None
        assert _validate_required("12345", "CI") is None

    def test_validate_required_empty_raises(self):
        with pytest.raises(ValueError, match="obligatorio"):
            _validate_required("", "Nombre")

    def test_validate_required_none_raises(self):
        with pytest.raises(ValueError, match="obligatorio"):
            _validate_required(None, "Apellido")

    def test_validate_int_invalid_raises(self):
        with pytest.raises(ValueError, match="número entero"):
            _validate_int("abc", "Edad")

    def test_validate_float_invalid_raises(self):
        with pytest.raises(ValueError, match="número"):
            _validate_float("not_a_number", "Costo")


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
