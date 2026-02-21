# Fix Silent Exception Swallowing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace bare `except: pass` blocks in `GXDLMSTranslator.py` and `GXDLMSReader.py` with proper logging and `writeTrace` calls so failures become observable.

**Architecture:** Library code uses Python's `logging` module with `logger.debug(..., exc_info=True)` — zero behavioral change, failures become visible when the caller enables debug logging. Example app code uses the existing `self.writeTrace()` pattern already present throughout `GXDLMSReader.py`.

**Tech Stack:** Python 3, `logging` (stdlib), `pytest`, `unittest.mock`

---

## Context

There are no existing tests in this repo. We bootstrap a minimal pytest setup in Task 1.

The silent exception sites are:

| File | Lines | Context |
|---|---|---|
| `GXDLMSTranslator.py` | 1173–1175 | Decryption attempt for GLO_CIPHERING XML comment |
| `GXDLMSTranslator.py` | 1209–1212 | Decryption attempt for GENERAL_GLO_CIPHERING XML comment |
| `GXDLMSReader.py` | 126–127 | `release()` — release request; not all meters support it |
| `GXDLMSReader.py` | 144–145 | `close()` — same release request pattern |
| `GXDLMSReader.py` | 501–502 | Reading individual register scaler/unit attribute |

All other `pass` statements in `GXDLMSTranslator.py` are in if-elif tag routing chains and are intentional — do not touch them.

---

### Task 1: Bootstrap pytest infrastructure

**Files:**
- Create: `Gurux.DLMS.python/tests/__init__.py`
- Create: `Gurux.DLMS.python/tests/test_translator_logging.py`
- Create: `Gurux.DLMS.python/setup.cfg`

**Step 1: Install pytest (if not already installed)**

```bash
pip install pytest
```

Expected: `Successfully installed pytest-...` or `Requirement already satisfied`

**Step 2: Create the tests package**

```bash
mkdir -p Gurux.DLMS.python/tests
touch Gurux.DLMS.python/tests/__init__.py
```

**Step 3: Create `setup.cfg` so pytest can find the package**

Create `Gurux.DLMS.python/setup.cfg`:

```ini
[tool:pytest]
testpaths = tests
```

**Step 4: Write the failing test for translator logging**

Create `Gurux.DLMS.python/tests/test_translator_logging.py`:

```python
import logging
from unittest.mock import patch, MagicMock
import sys
import os

# Make sure the library is importable from the tests directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator


def test_decrypt_failure_for_glo_ciphering_comment_is_logged(caplog):
    """When decryption fails during GLO_CIPHERING comment generation,
    a debug log message should be emitted instead of silently swallowing
    the exception."""
    translator = GXDLMSTranslator()
    translator.comments = True

    # Patch GXCiphering.decrypt to raise an exception (simulates wrong keys)
    with patch(
        'gurux_dlms.GXDLMSTranslator.GXCiphering.decrypt',
        side_effect=Exception("Decryption failed: invalid key")
    ):
        with caplog.at_level(logging.DEBUG, logger='gurux_dlms.GXDLMSTranslator'):
            # Build minimal cipher context so the code reaches the decrypt call
            mock_cipher = MagicMock()
            mock_cipher.blockCipherKey = b'\x00' * 16
            mock_cipher.authenticationKey = b'\x00' * 16
            mock_cipher.systemTitle = b'\x00' * 8

            # Call the internal method that contains the silent except block.
            # We use a minimal GXDLMSXmlSettings-like object.
            from gurux_dlms.GXDLMSSettings import GXDLMSSettings
            settings = GXDLMSSettings(True)
            settings.cipher = mock_cipher

            xml = MagicMock()
            xml.getXmlLength.return_value = 0

            from gurux_dlms.GXByteBuffer import GXByteBuffer
            from gurux_dlms.enums import Command

            value = GXByteBuffer()
            # Minimal GLO_CIPHERING payload (security byte + length + data)
            value.set(bytearray([0x00, 0x01, 0x00]))

            try:
                translator._pduToXml2(xml, value, True, True, False)
            except Exception:
                pass  # We only care that the log was emitted, not the parse result

    assert any(
        "decrypt" in record.message.lower() or "cipher" in record.message.lower()
        for record in caplog.records
        if record.levelno == logging.DEBUG
    ), "Expected a debug log message about decryption failure, but none was found"


def test_decrypt_failure_for_general_glo_ciphering_comment_is_logged(caplog):
    """Same as above but for the GENERAL_GLO_CIPHERING branch."""
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

            from gurux_dlms.GXDLMSSettings import GXDLMSSettings
            settings = GXDLMSSettings(True)
            settings.cipher = mock_cipher

            xml = MagicMock()
            xml.getXmlLength.return_value = 0

            from gurux_dlms.GXByteBuffer import GXByteBuffer

            value = GXByteBuffer()
            value.set(bytearray([0x00, 0x01, 0x00]))

            try:
                translator._pduToXml2(xml, value, True, True, False)
            except Exception:
                pass

    assert any(
        "decrypt" in record.message.lower() or "cipher" in record.message.lower()
        for record in caplog.records
        if record.levelno == logging.DEBUG
    ), "Expected a debug log message about decryption failure, but none was found"
```

**Step 5: Run the test to confirm it FAILS**

```bash
cd Gurux.DLMS.python && pytest tests/test_translator_logging.py -v
```

Expected: Both tests FAIL — `AssertionError: Expected a debug log message ...`

**Step 6: Commit the test setup**

```bash
git add Gurux.DLMS.python/tests/ Gurux.DLMS.python/setup.cfg
git commit -m "test: bootstrap pytest and add failing tests for translator logging"
```

---

### Task 2: Add logging to `GXDLMSTranslator.py`

**Files:**
- Modify: `Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py:34` (add import)
- Modify: `Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py:87` (add module logger)
- Modify: `Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py:1173` (first except block)
- Modify: `Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py:1209` (second except block)

**Step 1: Add `import logging` after the existing imports**

In `GXDLMSTranslator.py`, find the line:

```python
from __future__ import print_function
import xml.etree.cElementTree as ET
```

Add `import logging` immediately after the `import xml.etree.cElementTree as ET` line:

```python
from __future__ import print_function
import logging
import xml.etree.cElementTree as ET
```

**Step 2: Add the module-level logger just before the class definition**

The class definition is at line 88: `class GXDLMSTranslator:`. Add one line immediately above it:

```python
logger = logging.getLogger(__name__)


class GXDLMSTranslator:
```

**Step 3: Fix the first silent except block (GLO_CIPHERING, ~line 1173)**

Find this exact block:

```python
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not correct.
                    xml.xml.setXmlLength(len_)
```

Replace with:

```python
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not correct.
                    logger.debug("Failed to decrypt GLO_CIPHERING data for XML comment", exc_info=True)
                    xml.xml.setXmlLength(len_)
```

**Step 4: Fix the second silent except block (GENERAL_GLO_CIPHERING, ~line 1209)**

Find this exact block:

```python
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not
                    #  correct.
                    xml.setXmlLength(len_)
```

Replace with:

```python
                except Exception:
                    #  It's OK if this fails.  Ciphering settings are not
                    #  correct.
                    logger.debug("Failed to decrypt GENERAL_GLO_CIPHERING data for XML comment", exc_info=True)
                    xml.setXmlLength(len_)
```

**Step 5: Run the tests — they should now PASS**

```bash
cd Gurux.DLMS.python && pytest tests/test_translator_logging.py -v
```

Expected output:
```
PASSED tests/test_translator_logging.py::test_decrypt_failure_for_glo_ciphering_comment_is_logged
PASSED tests/test_translator_logging.py::test_decrypt_failure_for_general_glo_ciphering_comment_is_logged
```

**Step 6: Commit**

```bash
git add Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py
git commit -m "fix: log decryption failures in GXDLMSTranslator instead of silently swallowing"
```

---

### Task 3: Fix silent exceptions in `GXDLMSReader.py`

Note: `GXDLMSReader.py` is an example application that requires a live media connection to test end-to-end. We do not write unit tests for it. The fix is mechanical — replace `pass` with `self.writeTrace(...)` to match the existing pattern used throughout the file.

**Files:**
- Modify: `Gurux.DLMS.Client.Example.python/GXDLMSReader.py:126`
- Modify: `Gurux.DLMS.Client.Example.python/GXDLMSReader.py:144`
- Modify: `Gurux.DLMS.Client.Example.python/GXDLMSReader.py:501`

**Step 1: Fix `release()` — lines 125–128**

Find this exact block in `GXDLMSReader.py`:

```python
            except Exception:
                pass
                #  All meters don't support release.
```

(This is in the `release()` method, around line 126.)

Replace with:

```python
            except Exception as e:
                #  All meters don't support release.
                self.writeTrace("Release request failed (meter may not support it): " + str(e), TraceLevel.WARNING)
```

**Step 2: Fix `close()` — lines 143–146**

Find the identical block in the `close()` method (around line 144):

```python
            except Exception:
                pass
                #  All meters don't support release.
```

Replace with:

```python
            except Exception as e:
                #  All meters don't support release.
                self.writeTrace("Release request failed (meter may not support it): " + str(e), TraceLevel.WARNING)
```

**Step 3: Fix `readScalerAndUnits()` — lines 500–502**

Find this block (around line 501):

```python
                except Exception:
                    pass
```

Replace with:

```python
                except Exception as e:
                    self.writeTrace("Failed to read scaler/unit for " + str(it.name) + ": " + str(e), TraceLevel.WARNING)
```

**Step 4: Verify the file is syntactically correct**

```bash
python -m py_compile Gurux.DLMS.Client.Example.python/GXDLMSReader.py && echo "OK"
```

Expected: `OK`

**Step 5: Run all tests to make sure nothing broke**

```bash
cd Gurux.DLMS.python && pytest tests/ -v
```

Expected: All tests PASS.

**Step 6: Commit**

```bash
git add Gurux.DLMS.Client.Example.python/GXDLMSReader.py
git commit -m "fix: replace silent exception swallowing in GXDLMSReader with writeTrace warnings"
```

---

### Task 4: Final verification

**Step 1: Run the full test suite one last time**

```bash
cd Gurux.DLMS.python && pytest tests/ -v
```

Expected: All tests PASS, no warnings about missing imports.

**Step 2: Verify the translator's logging name is correct**

```bash
python -c "from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator; import logging; logging.basicConfig(level=logging.DEBUG); t = GXDLMSTranslator(); print('Import OK')"
```

Expected: `Import OK`

**Step 3: Commit if clean**

```bash
git status
```

If nothing extra is staged, you're done. If any stray files appeared, investigate before committing.
