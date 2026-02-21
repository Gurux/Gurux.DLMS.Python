# Design: Fix Silent Exception Swallowing

**Date:** 2026-02-20
**Scope:** `GXDLMSTranslator.py` (library) + `GXDLMSReader.py` (example)

---

## Problem

Several `except` blocks in the codebase swallow exceptions silently — either with bare
`pass` or with no diagnostic output. This makes debugging meter communication failures
very difficult because errors vanish without a trace.

---

## Findings

Most `pass` statements in `GXDLMSTranslator.py` are **intentional no-ops** in large
if-elif tag routing chains (XML tag dispatch). These are correct and are not changed.

The actual silent exception sites are:

| File | Lines | Context |
|---|---|---|
| `GXDLMSTranslator.py` | ~1173, ~1209 | Decryption attempt for inline XML comment output fails silently |
| `GXDLMSReader.py` | ~126–127, ~144–145 | Release request on disconnect — not all meters support it |
| `GXDLMSReader.py` | ~501–502 | Reading individual register scaler/unit attribute fails silently |

---

## Approach: Add logging (no behavioral change)

### Library — `GXDLMSTranslator.py`

- Add `import logging` and `logger = logging.getLogger(__name__)` at module level.
- In each silent decrypt-attempt except block, add `logger.debug(...)` with `exc_info=True`
  before the existing XML-rollback line.
- The rollback behavior is preserved. The change only makes the failure observable when
  the caller enables debug logging.

### Examples — `GXDLMSReader.py`

- The example already uses `self.writeTrace(message, TraceLevel.X)` for all output.
- Replace each bare `except Exception: pass` with a `self.writeTrace("...", TraceLevel.WARNING)`
  call to stay consistent with the existing pattern.

---

## Non-goals

- Do not touch `pass` statements inside if-elif chains — they are correct.
- Do not change error-handling in other files (separate contribution).
- Do not introduce a `strict` mode flag — out of scope for this change.

---

## Files Changed

1. `Gurux.DLMS.python/gurux_dlms/GXDLMSTranslator.py`
2. `Gurux.DLMS.Client.Example.python/GXDLMSReader.py`
