import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from database.crypto import encrypt_field, decrypt_field, KEY_PATH


class TestCrypto:
    def test_encrypt_decrypt_roundtrip(self):
        original = "Hello World"
        encrypted = encrypt_field(original)
        decrypted = decrypt_field(encrypted)
        assert decrypted == original

    def test_unicode_characters(self):
        original = "José García - Ñoño - 你好"
        encrypted = encrypt_field(original)
        decrypted = decrypt_field(encrypted)
        assert decrypted == original

    def test_decrypt_invalid_token_returns_original(self):
        result = decrypt_field("invalid_token_12345")
        assert result == "invalid_token_12345"

    def test_decrypt_token_from_other_key_returns_empty(self):
        """Un token cifrado con OTRA clave no debe devolverse en crudo
        (evita re-cifrar basura si la clave se perdio)."""
        import base64
        from cryptography.fernet import Fernet
        other = Fernet(Fernet.generate_key())
        token = other.encrypt("secreto".encode("utf-8"))
        value = base64.urlsafe_b64encode(token).decode("utf-8")
        assert decrypt_field(value) == ""
