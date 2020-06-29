# st2common

import os

import six
import json
import binascii

from six.moves import range
from cryptography.exceptions import InvalidSignature

from ultron8.utils.crypto import KEYCZAR_HEADER_SIZE
from ultron8.utils.crypto import AESKey
from ultron8.utils.crypto import read_crypto_key
from ultron8.utils.crypto import symmetric_encrypt
from ultron8.utils.crypto import symmetric_decrypt
from ultron8.utils.crypto import cryptography_symmetric_encrypt
from ultron8.utils.crypto import cryptography_symmetric_decrypt

import pytest

# from st2tests.fixturesloader import get_fixtures_base_path

from tests.conftest import fixtures_path

__all__ = ["CryptoUtilsTestCase", "CryptoUtilsKeyczarCompatibilityTestCase"]

KEY_FIXTURES_PATH = fixtures_path / "keyczar_keys/"


class CryptoUtilsTestCase:
    test_crypto_key = AESKey.generate()

    # @classmethod
    # def setUpClass(cls):

    #     CryptoUtilsTestCase.test_crypto_key = AESKey.generate()

    def test_symmetric_encrypt_decrypt_short_string_needs_to_be_padded(self):
        original = u"a"
        crypto = symmetric_encrypt(CryptoUtilsTestCase.test_crypto_key, original)
        plain = symmetric_decrypt(CryptoUtilsTestCase.test_crypto_key, crypto)
        assert plain == original

    def test_symmetric_encrypt_decrypt_utf8_character(self):
        values = [
            u"£",
            u"£££",
            u"££££££",
            u"č š hello đ č p ž Ž",
            u"hello 💩",
            u"💩💩💩💩💩" u"💩💩💩",
            u"💩😁",
        ]

        for index, original in enumerate(values):
            crypto = symmetric_encrypt(CryptoUtilsTestCase.test_crypto_key, original)
            plain = symmetric_decrypt(CryptoUtilsTestCase.test_crypto_key, crypto)
            assert plain == original

        assert index == (len(values) - 1)

    def test_symmetric_encrypt_decrypt(self):
        original = "secret"
        crypto = symmetric_encrypt(CryptoUtilsTestCase.test_crypto_key, original)
        plain = symmetric_decrypt(CryptoUtilsTestCase.test_crypto_key, crypto)
        assert plain == original

    def test_encrypt_output_is_diff_due_to_diff_IV(self):
        original = "Kami is a little boy."
        cryptos = set()

        for _ in range(0, 10000):
            crypto = symmetric_encrypt(CryptoUtilsTestCase.test_crypto_key, original)
            assert crypto not in cryptos
            cryptos.add(crypto)

    def test_decrypt_ciphertext_is_too_short(self):
        aes_key = AESKey.generate()
        plaintext = "hello world ponies 1"
        encrypted = cryptography_symmetric_encrypt(aes_key, plaintext)

        # Verify original non manipulated value can be decrypted
        decrypted = cryptography_symmetric_decrypt(aes_key, encrypted)
        assert decrypted == plaintext

        # Corrupt / shortern the encrypted data
        encrypted_malformed = binascii.unhexlify(encrypted)
        header = encrypted_malformed[:KEYCZAR_HEADER_SIZE]
        encrypted_malformed = encrypted_malformed[KEYCZAR_HEADER_SIZE:]

        # Remove 40 bytes from ciphertext bytes
        encrypted_malformed = encrypted_malformed[40:]

        # Add back header
        encrypted_malformed = header + encrypted_malformed
        encrypted_malformed = binascii.hexlify(encrypted_malformed)

        # Verify corrupted value results in an excpetion
        expected_msg = "Invalid or malformed ciphertext"
        with pytest.raises(ValueError, match=expected_msg):
            cryptography_symmetric_decrypt(aes_key, encrypted_malformed)

    def test_exception_is_thrown_on_invalid_hmac_signature(self):
        aes_key = AESKey.generate()
        plaintext = "hello world ponies 2"
        encrypted = cryptography_symmetric_encrypt(aes_key, plaintext)

        # Verify original non manipulated value can be decrypted
        decrypted = cryptography_symmetric_decrypt(aes_key, encrypted)
        assert decrypted == plaintext

        # Corrupt the HMAC signature (last part is the HMAC signature)
        encrypted_malformed = binascii.unhexlify(encrypted)
        encrypted_malformed = encrypted_malformed[:-3]
        encrypted_malformed += b"abc"
        encrypted_malformed = binascii.hexlify(encrypted_malformed)

        # Verify corrupted value results in an excpetion
        expected_msg = "Signature did not match digest"
        with pytest.raises(InvalidSignature, match=expected_msg):
            cryptography_symmetric_decrypt(aes_key, encrypted_malformed)


class CryptoUtilsKeyczarCompatibilityTestCase:
    """
    Tests which verify that new cryptography based symmetric_encrypt and symmetric_decrypt are
    fully compatible with keyczar output format and also return keyczar based format.
    """

    def test_aes_key_class(self):
        # 1. Unsupported mode
        expected_msg = "Unsupported mode: EBC"
        with pytest.raises(ValueError, match=expected_msg):
            AESKey(
                aes_key_string="a", hmac_key_string="b", hmac_key_size=128, mode="EBC"
            )

        # 2. AES key is too small
        expected_msg = "Unsafe key size: 64"
        with pytest.raises(ValueError, match=expected_msg):
            AESKey(
                aes_key_string="a",
                hmac_key_string="b",
                hmac_key_size=128,
                mode="CBC",
                size=64,
            )

    def test_loading_keys_from_keyczar_formatted_key_files(self):
        key_path = os.path.join(KEY_FIXTURES_PATH, "one.json")
        aes_key = read_crypto_key(key_path=key_path)

        assert aes_key.hmac_key_string == "lgI9YdOKlIOtPQFdgB0B6zr0AZ6L2QJuFQg4gTu2dxc"
        assert aes_key.hmac_key_size == 256

        assert aes_key.aes_key_string == "vKmBE2YeQ9ATyovel7NDjdnbvOMcoU5uPtUVxWxWm58"
        assert aes_key.mode == "CBC"
        assert aes_key.size == 256

        key_path = os.path.join(KEY_FIXTURES_PATH, "two.json")
        aes_key = read_crypto_key(key_path=key_path)

        assert aes_key.hmac_key_string == "92ok9S5extxphADmUhObPSD5wugey8eTffoJ2CEg_2s"
        assert aes_key.hmac_key_size == 256

        assert aes_key.aes_key_string == "fU9hT9pm-b9hu3VyQACLXe2Z7xnaJMZrXiTltyLUzgs"
        assert aes_key.mode == "CBC"
        assert aes_key.size == 256

        key_path = os.path.join(KEY_FIXTURES_PATH, "five.json")
        aes_key = read_crypto_key(key_path=key_path)

        assert aes_key.hmac_key_string == "GCX2uMfOzp1JXYgqH8piEE4_mJOPXydH_fRHPDw9bkM"
        assert aes_key.hmac_key_size == 256

        assert aes_key.aes_key_string == "EeBcUcbH14tL0w_fF5siEw"
        assert aes_key.mode == "CBC"
        assert aes_key.size == 128

    def test_key_generation_file_format_is_fully_keyczar_compatible(self):
        # Verify that the code can read and correctly parse keyczar formatted key files
        aes_key = AESKey.generate()
        key_json = aes_key.to_json()
        json_parsed = json.loads(key_json)

        expected = {
            "hmacKey": {
                "hmacKeyString": aes_key.hmac_key_string,
                "size": aes_key.hmac_key_size,
            },
            "aesKeyString": aes_key.aes_key_string,
            "mode": aes_key.mode,
            "size": aes_key.size,
        }

        assert json_parsed == expected

    def test_symmetric_encrypt_decrypt_cryptography(self):
        key = AESKey.generate()
        plaintexts = [
            "a b c",
            "ab",
            "hello foo",
            "hell",
            "bar5" "hello hello bar bar hello",
            "a",
            "",
            "c",
        ]

        for plaintext in plaintexts:
            encrypted = cryptography_symmetric_encrypt(key, plaintext)
            decrypted = cryptography_symmetric_decrypt(key, encrypted)

            assert decrypted == plaintext
