import logging
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator


def test_decrypt_failure_for_glo_ciphering_comment_is_logged(caplog):
    """When decryption fails during GLO_CIPHERING comment generation,
    a debug log message should be emitted instead of silently swallowing
    the exception."""
    translator = GXDLMSTranslator()
    translator.comments = True

    with patch(
        'gurux_dlms.GXDLMSTranslator.GXCiphering.decrypt',
        side_effect=Exception("Decryption failed: invalid key")
    ):
        with caplog.at_level(logging.DEBUG, logger='gurux_dlms.GXDLMSTranslator'):
            mock_cipher = MagicMock()
            mock_cipher.blockCipherKey = b'\x00' * 16
            mock_cipher.authenticationKey = b'\x00' * 16
            mock_cipher.systemTitle = b'\x00' * 8

            from gurux_dlms.GXByteBuffer import GXByteBuffer

            value = GXByteBuffer()
            value.set(bytearray([0x00, 0x01, 0x00]))

            try:
                translator._pduToXml2(MagicMock(), value, True, True, False)
            except Exception:
                pass

    assert any(
        "decrypt" in record.message.lower() or "cipher" in record.message.lower()
        for record in caplog.records
        if record.levelno == logging.DEBUG
    ), "Expected a debug log message about decryption failure, but none was found"


def test_decrypt_failure_for_general_glo_ciphering_comment_is_logged(caplog):
    """When decryption fails during GENERAL_GLO_CIPHERING comment generation,
    a debug log message should be emitted."""
    translator = GXDLMSTranslator()
    translator.comments = True

    with patch(
        'gurux_dlms.GXDLMSTranslator.GXCiphering.decrypt',
        side_effect=Exception("Decryption failed: invalid key")
    ):
        with caplog.at_level(logging.DEBUG, logger='gurux_dlms.GXDLMSTranslator'):
            mock_cipher = MagicMock()
            mock_cipher.blockCipherKey = b'\x00' * 16
            mock_cipher.authenticationKey = b'\x00' * 16
            mock_cipher.systemTitle = b'\x00' * 8

            from gurux_dlms.GXByteBuffer import GXByteBuffer

            value = GXByteBuffer()
            value.set(bytearray([0x00, 0x01, 0x00]))

            try:
                translator._pduToXml2(MagicMock(), value, True, True, False)
            except Exception:
                pass

    assert any(
        "decrypt" in record.message.lower() or "cipher" in record.message.lower()
        for record in caplog.records
        if record.levelno == logging.DEBUG
    ), "Expected a debug log message about decryption failure, but none was found"
