import os
import sys
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import createRow_PACIENTES, createRow_ABONO
from database.utils import readTable_PACIENTES_ordered, readPATIENTS_with_remaining_all


class TestDatabasePerformance:
    def test_insert_and_query_100_records(self, test_db):
        start = time.time()
        for i in range(100):
            createRow_PACIENTES(
                f"Paciente{i}", f"Apellido{i}", 30, f"{i:08d}",
                "2024-01-15", "099123", "Dir", "Rep", "RepCI", "Motivo", "Sintomas"
            )
            createRow_ABONO(i + 1, "2024-01-01", "Limpieza", 100.0, 50.0, 50.0)
        insert_time = time.time() - start

        start = time.time()
        for _ in range(10):
            readTable_PACIENTES_ordered()
            readPATIENTS_with_remaining_all()
        query_time = time.time() - start

        assert insert_time < 3.0, f"Inserts took {insert_time:.2f}s"
        assert query_time < 2.0, f"Queries took {query_time:.2f}s"
