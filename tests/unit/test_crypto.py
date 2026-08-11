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

    def test_empty_string_untouched(self):
        assert encrypt_field("") == ""
        assert decrypt_field("") == ""

    def test_unicode_characters(self):
        original = "José García - Ñoño - 你好"
        encrypted = encrypt_field(original)
        decrypted = decrypt_field(encrypted)
        assert decrypted == original

    def test_different_encryptions_different_output(self):
        enc1 = encrypt_field("Same Input")
        enc2 = encrypt_field("Same Input")
        assert enc1 != enc2

    def test_decrypt_invalid_token_returns_original(self):
        result = decrypt_field("invalid_token_12345")
        assert result == "invalid_token_12345"
