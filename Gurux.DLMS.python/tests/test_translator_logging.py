import logging
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator


def test_decrypt_failure_for_glo_ciphering_comment_is_logged(caplog):
    """When decryption fails during GLO_CIPHERING comment generation,
    a debug log message should be emitted instead of silently swallowing
    the exception."""
    # Command.GLO_GET_REQUEST = 0xC8 triggers the GLO ciphering branch in _pduToXml2
    translator = GXDLMSTranslator()
    translator.comments = True

    with patch(
        'gurux_dlms.GXDLMSTranslator.GXCiphering.decrypt',
        side_effect=Exception("Decryption failed: invalid key")
    ):
        with caplog.at_level(logging.DEBUG, logger='gurux_dlms.GXDLMSTranslator'):
            value = GXByteBuffer()
            value.set(bytearray([0xC8, 0x01, 0x00]))

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
    # Command.GENERAL_GLO_CIPHERING = 0xDB triggers the general GLO ciphering branch
    translator = GXDLMSTranslator()
    translator.comments = True

    with patch(
        'gurux_dlms.GXDLMSTranslator.GXCiphering.decrypt',
        side_effect=Exception("Decryption failed: invalid key")
    ):
        with caplog.at_level(logging.DEBUG, logger='gurux_dlms.GXDLMSTranslator'):
            value = GXByteBuffer()
            value.set(bytearray([0xDB, 0x01, 0x00]))

            try:
                translator._pduToXml2(MagicMock(), value, True, True, False)
            except Exception:
                pass

    assert any(
        "decrypt" in record.message.lower() or "cipher" in record.message.lower()
        for record in caplog.records
        if record.levelno == logging.DEBUG
    ), "Expected a debug log message about decryption failure, but none was found"
