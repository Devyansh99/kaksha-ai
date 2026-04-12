---
phase: 2
slug: resilient-misconception-extraction
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-04-12
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none — existing phase tests are direct pytest |
| **Quick run command** | `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py -q` |
| **Full suite command** | `venv\Scripts\python -m pytest -q` |
| **Estimated runtime** | ~25 seconds |

---

## Sampling Rate

- **After every task commit:** Run `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py -q`
- **After every plan wave:** Run `venv\Scripts\python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 2-01-01 | 01 | 1 | LLM-01 | T-02-01 | JSON-only contract enforced at prompt and parser boundary | unit | `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py::test_prompt_requires_json_only_contract -q` | ✅ | ⬜ pending |
| 2-01-02 | 01 | 1 | LLM-02 | T-02-02 | OpenRouter key/model loaded from env and used via centralized client | unit | `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py::test_openrouter_client_uses_env_config -q` | ✅ | ⬜ pending |
| 2-02-01 | 02 | 2 | LLM-03 | T-02-03 | Timeout/service failures trigger bounded retries and structured failure output | integration | `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py::test_retry_timeout_is_bounded_and_non_crashing -q` | ✅ | ⬜ pending |
| 2-02-02 | 02 | 2 | LLM-04 | T-02-04 | Malformed JSON triggers one repair then deterministic fallback | integration | `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py::test_malformed_json_repair_then_fallback -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠ flaky*

---

## Wave 0 Requirements

- Existing infrastructure covers all phase requirements.

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
