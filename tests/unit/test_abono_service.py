import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.abono_service import add_abono, get_patient_abonos
from database.createDB import createRow_ABONO


class TestAddAbono:
    def test_add_abono_valid(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 0.0, 100.0)
        result = add_abono(created_patient, "50.0", "2024-01-15", "Pago")
        assert result["remaining"] == 50.0

    def test_add_abono_zero_amount(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 0.0, 100.0)
        result = add_abono(created_patient, "0", "2024-01-15", "Pago")
        assert result["remaining"] == 100.0

    def test_add_abono_negative_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 0.0, 100.0)
        with pytest.raises(ValueError, match="negativo"):
            add_abono(created_patient, "-50", "2024-01-15", "Pago")

    def test_calculate_remaining_cumulative(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 0.0, 100.0)
        add_abono(created_patient, "30.0", "2024-01-10", "Pago 1")
        result = add_abono(created_patient, "20.0", "2024-01-15", "Pago 2")
        assert result["remaining"] == 50.0

    def test_abono_exceeds_remaining_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 0.0, 100.0)
        with pytest.raises(ValueError, match="excede"):
            add_abono(created_patient, "150.0", "2024-01-15", "Pago")


class TestGetAbonos:
    def test_get_patient_abonos(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Limpieza", 100.0, 50.0, 50.0)
        abonos = get_patient_abonos(created_patient)
        assert len(abonos) == 1
        assert abonos[0].remaining == 50.0

    def test_abonos_ordered_by_date_desc(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Pago 1", 100.0, 30.0, 70.0)
        createRow_ABONO(created_patient, "2024-01-15", "Pago 2", 100.0, 20.0, 50.0)
        abonos = get_patient_abonos(created_patient)
        assert len(abonos) == 2
        assert abonos[0].date == "2024-01-15"
