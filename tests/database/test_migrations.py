import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.createDB import getConnection
from database.migrations import (
    run_migrations, get_schema_version, LATEST_SCHEMA_VERSION
)


class TestMigrations:
    def test_run_migrations_sets_latest_version(self, test_db):
        run_migrations()
        assert get_schema_version() == LATEST_SCHEMA_VERSION

    def test_migrations_are_idempotent(self, test_db):
        run_migrations()
        run_migrations()
        assert get_schema_version() == LATEST_SCHEMA_VERSION

    def test_tratamiento_has_date_column(self, test_db):
        run_migrations()
        conn = getConnection()
        try:
            cursor = conn.execute("PRAGMA table_info(tratamiento)")
            columns = [col[1] for col in cursor.fetchall()]
            assert "date" in columns
        finally:
            conn.close()

    def test_baseline_tables_exist(self, test_db):
        run_migrations()
        conn = getConnection()
        try:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {r[0] for r in cursor.fetchall()}
            expected = {
                "pacientes", "antecedentes_personales", "examen_fisico",
                "odontograms", "odontogram_details", "tratamiento", "abonos",
            }
            assert expected.issubset(tables)
        finally:
            conn.close()
