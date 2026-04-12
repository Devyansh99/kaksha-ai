---
phase: 1
slug: data-contracts-and-cleaning
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-04-12
---

# Phase 1 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none — Wave 0 installs |
| **Quick run command** | `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py -q` |
| **Full suite command** | `venv\Scripts\python -m pytest -q` |
| **Estimated runtime** | ~20 seconds |

---

## Sampling Rate

- **After every task commit:** Run `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py -q`
- **After every plan wave:** Run `venv\Scripts\python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 1 | DATA-01 | T-01-01 | Reject malformed required fields | unit | `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py::test_missing_required_fields_are_dropped -q` | ✅ | ⬜ pending |
| 1-01-02 | 01 | 1 | DATA-02 | T-01-02 | Normalize timestamps to UTC ISO-8601 | unit | `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py::test_timestamp_normalization_to_utc_iso -q` | ✅ | ⬜ pending |
| 1-02-01 | 02 | 2 | DATA-04 | T-01-03 | Forward only strict incorrect rows | unit | `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py::test_only_incorrect_rows_forwarded -q` | ✅ | ⬜ pending |
| 1-02-02 | 02 | 2 | DATA-03 | T-01-04 | Produce structured drop logs with reason codes | integration | `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py::test_drop_log_written_with_reason_codes -q` | ✅ | ⬜ pending |

*Status: ⬜ pending - ✅ green - ❌ red - ⚠ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_data_contracts_and_cleaning.py` — scaffold tests for DATA-01 to DATA-04
- [ ] `venv\Scripts\python -m pip install pytest pandas python-dateutil` — install test/runtime deps inside venv

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
