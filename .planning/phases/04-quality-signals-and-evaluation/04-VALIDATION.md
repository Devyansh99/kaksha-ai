---
phase: 4
slug: quality-signals-and-evaluation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-12
---

# Phase 4 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none - direct pytest modules |
| **Quick run command** | `venv\Scripts\python -m pytest tests/test_quality_signals.py tests/test_prompt_strategy_comparison.py -q` |
| **Full suite command** | `venv\Scripts\python -m pytest -q` |
| **Estimated runtime** | ~40 seconds |

---

## Sampling Rate

- **After every task commit:** Run `venv\Scripts\python -m pytest tests/test_quality_signals.py tests/test_prompt_strategy_comparison.py -q`
- **After every plan wave:** Run `venv\Scripts\python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 45 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 4-01-01 | 01 | 1 | QLT-01 | T-04-01 | Deterministic taxonomy mapping with explicit fallback reason | unit | `venv\Scripts\python -m pytest tests/test_quality_signals.py::test_normalize_label_maps_aliases_deterministically -q` | ✅ | ⬜ pending |
| 4-01-02 | 01 | 1 | QLT-03 | T-04-02 | Confidence visibility includes rounded score and confidence band | integration | `venv\Scripts\python -m pytest tests/test_quality_signals.py::test_report_includes_normalized_labels_and_confidence_bands -q` | ✅ | ⬜ pending |
| 4-02-01 | 02 | 2 | QLT-02 | T-04-03 | Prompt strategy builders remain strict-JSON and deterministic | unit | `venv\Scripts\python -m pytest tests/test_prompt_strategy_comparison.py::test_prompt_strategy_builders_are_distinct_and_json_strict -q` | ✅ | ⬜ pending |
| 4-02-02 | 02 | 2 | QLT-02 | T-04-04 | Strategy comparison summary contains required metrics and deterministic ordering | integration | `venv\Scripts\python -m pytest tests/test_prompt_strategy_comparison.py::test_strategy_comparison_summary_contains_required_metrics -q` | ✅ | ⬜ pending |

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
- [ ] Feedback latency < 45s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** planner-ready
