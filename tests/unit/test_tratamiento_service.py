import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.tratamiento_service import (
    add_tratamiento, update_tratamiento, delete_tratamiento,
    get_patient_tratamientos
)


class TestAddTratamiento:
    def test_add_tratamiento_valid(self, test_db, created_patient):
        tid = add_tratamiento(created_patient, "Limpieza dental", "2024-01-15")
        assert tid is not None and tid > 0

        rows = get_patient_tratamientos(created_patient)
        assert len(rows) == 1
        assert rows[0].diagnosis == "Limpieza dental"
        assert rows[0].date == "2024-01-15"

    def test_add_tratamiento_empty_text_raises(self, test_db, created_patient):
        with pytest.raises(ValueError, match="obligatorio"):
            add_tratamiento(created_patient, "   ", "2024-01-15")

    def test_tratamientos_ordered_by_date_desc(self, test_db, created_patient):
        add_tratamiento(created_patient, "Primero", "2024-01-10")
        add_tratamiento(created_patient, "Segundo", "2024-02-10")
        rows = get_patient_tratamientos(created_patient)
        assert rows[0].diagnosis == "Segundo"
        assert rows[1].diagnosis == "Primero"


class TestUpdateTratamiento:
    def test_update_tratamiento(self, test_db, created_patient):
        tid = add_tratamiento(created_patient, "Texto original", "2024-01-15")
        update_tratamiento(tid, "Texto corregido", "2024-01-20")

        rows = get_patient_tratamientos(created_patient)
        assert len(rows) == 1
        assert rows[0].diagnosis == "Texto corregido"
        assert rows[0].date == "2024-01-20"

    def test_update_tratamiento_empty_text_raises(self, test_db, created_patient):
        tid = add_tratamiento(created_patient, "Texto", "2024-01-15")
        with pytest.raises(ValueError, match="obligatorio"):
            update_tratamiento(tid, "", "2024-01-15")


class TestDeleteTratamiento:
    def test_delete_tratamiento(self, test_db, created_patient):
        tid = add_tratamiento(created_patient, "A borrar", "2024-01-15")
        delete_tratamiento(tid)
        assert get_patient_tratamientos(created_patient) == []
