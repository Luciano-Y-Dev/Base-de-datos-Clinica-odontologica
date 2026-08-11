import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.abono_service import add_abono, get_patient_abonos, update_abono, delete_abono
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


class TestUpdateAbono:
    def test_update_abono_recalculates_following(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        add_abono(created_patient, "30.0", "2024-01-10", "Pago 1")
        add_abono(created_patient, "20.0", "2024-01-15", "Pago 2")

        middle = get_patient_abonos(created_patient)[1]  # Pago 1 (orden DESC)
        result = update_abono(created_patient, middle.id, "50.0", "2024-01-10", "Pago 1 corregido")

        assert result["remaining"] == 30.0
        abonos = get_patient_abonos(created_patient)
        assert abonos[0].remaining == 30.0   # Pago 2 recalculado
        assert abonos[1].remaining == 50.0   # Pago 1 corregido
        assert abonos[1].description == "Pago 1 corregido"

    def test_update_abono_negative_chain_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        first = get_patient_abonos(created_patient)[0]
        with pytest.raises(ValueError, match="negativo"):
            update_abono(created_patient, first.id, "150.0", "2024-01-01", "Excede")

    def test_update_nonexistent_abono_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        with pytest.raises(ValueError, match="no existe"):
            update_abono(created_patient, 999999, "10.0", "2024-01-01", "X")

    def test_update_abono_invalid_amount_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        first = get_patient_abonos(created_patient)[0]
        with pytest.raises(ValueError, match="número"):
            update_abono(created_patient, first.id, "abc", "2024-01-01", "X")


class TestDeleteAbono:
    def test_delete_middle_abono_recalculates(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        add_abono(created_patient, "30.0", "2024-01-10", "Pago 1")
        add_abono(created_patient, "20.0", "2024-01-15", "Pago 2")

        middle = get_patient_abonos(created_patient)[1]  # Pago 1
        result = delete_abono(created_patient, middle.id)

        assert result["remaining"] == 80.0
        abonos = get_patient_abonos(created_patient)
        assert len(abonos) == 2
        assert abonos[0].remaining == 80.0   # Pago 2 recalculado
        assert abonos[1].remaining == 100.0  # Inicial intacto

    def test_delete_only_abono_leaves_none(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 50.0, 50.0)
        only = get_patient_abonos(created_patient)[0]
        result = delete_abono(created_patient, only.id)
        assert result["remaining"] == 0.0
        assert get_patient_abonos(created_patient) == []

    def test_delete_nonexistent_abono_raises(self, test_db, created_patient):
        createRow_ABONO(created_patient, "2024-01-01", "Inicial", 100.0, 0.0, 100.0)
        with pytest.raises(ValueError, match="no existe"):
            delete_abono(created_patient, 999999)
