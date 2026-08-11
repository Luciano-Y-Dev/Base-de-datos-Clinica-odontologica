import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database import createDB, crypto
from services import backup_service


@pytest.fixture
def backup_env(tmp_path, monkeypatch):
    """Aísla las rutas de DB, clave y backups en una carpeta temporal."""
    db_path = tmp_path / "Clinica.db"
    db_path.write_bytes(b"fake-database-content")
    key_path = tmp_path / "secret.key"
    key_path.write_bytes(b"fake-key-content")
    backup_dir = tmp_path / "Backups"

    monkeypatch.setattr(createDB, "DB_PATH", str(db_path))
    monkeypatch.setattr(crypto, "KEY_PATH", str(key_path))
    monkeypatch.setattr(backup_service, "BACKUP_DIR", str(backup_dir))
    return {
        "db": db_path, "key": key_path, "backup_dir": backup_dir,
        "tmp": tmp_path,
    }


class TestCreateBackup:
    def test_backup_copies_db_and_key(self, backup_env):
        dest = backup_service.create_backup()
        assert os.path.exists(os.path.join(dest, "Clinica.db"))
        assert os.path.exists(os.path.join(dest, "secret.key"))
        with open(os.path.join(dest, "Clinica.db"), "rb") as f:
            assert f.read() == b"fake-database-content"

    def test_backup_to_custom_destination(self, backup_env):
        custom = backup_env["tmp"] / "usb"
        custom.mkdir()
        dest = backup_service.create_backup(str(custom))
        assert str(custom) in dest
        assert os.path.exists(os.path.join(dest, "Clinica.db"))

    def test_backup_missing_db_raises(self, backup_env):
        backup_env["db"].unlink()
        with pytest.raises(FileNotFoundError):
            backup_service.create_backup()


class TestRotation:
    def test_rotation_keeps_max_backups(self, backup_env, monkeypatch):
        monkeypatch.setattr(backup_service, "MAX_BACKUPS", 3)
        for _ in range(5):
            backup_service.create_backup()
        backups = [d for d in os.listdir(backup_env["backup_dir"]) if d.startswith("respaldo_")]
        assert len(backups) == 3

    def test_custom_destination_does_not_rotate(self, backup_env, monkeypatch):
        monkeypatch.setattr(backup_service, "MAX_BACKUPS", 1)
        custom = backup_env["tmp"] / "usb"
        custom.mkdir()
        backup_service.create_backup(str(custom))
        backup_service.create_backup(str(custom))
        backups = [d for d in os.listdir(custom) if d.startswith("respaldo_")]
        assert len(backups) == 2


class TestRestoreBackup:
    def test_restore_replaces_db_and_key(self, backup_env):
        dest = backup_service.create_backup()

        backup_env["db"].write_bytes(b"corrupted")
        backup_env["key"].write_bytes(b"corrupted-key")

        backup_service.restore_backup(dest)
        assert backup_env["db"].read_bytes() == b"fake-database-content"
        assert backup_env["key"].read_bytes() == b"fake-key-content"

    def test_restore_invalid_folder_raises(self, backup_env):
        empty = backup_env["tmp"] / "empty"
        empty.mkdir()
        with pytest.raises(FileNotFoundError, match="respaldo"):
            backup_service.restore_backup(str(empty))

    def test_restore_creates_safety_backup_first(self, backup_env):
        dest = backup_service.create_backup()
        backup_env["db"].write_bytes(b"current-state")
        backup_service.restore_backup(dest)
        # Ademas del respaldo original, debe existir uno de seguridad previo
        backups = [d for d in os.listdir(backup_env["backup_dir"]) if d.startswith("respaldo_")]
        assert len(backups) >= 2
