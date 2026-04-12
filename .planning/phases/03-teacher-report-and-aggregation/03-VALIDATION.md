---
phase: 3
slug: teacher-report-and-aggregation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-12
---

# Phase 3 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none - direct pytest test modules |
| **Quick run command** | `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py -q` |
| **Full suite command** | `venv\Scripts\python -m pytest -q` |
| **Estimated runtime** | ~25 seconds |

---

## Sampling Rate

- **After every task commit:** Run `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py -q`
- **After every plan wave:** Run `venv\Scripts\python -m pytest -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 3-01-01 | 01 | 1 | RPT-01 | T-03-01 | Mastery score deterministic and bounded [0,100] | unit | `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py::test_mastery_score_is_bounded_and_deterministic -q` | ✅ | ⬜ pending |
| 3-01-02 | 01 | 1 | RPT-03 | T-03-02 | Cohort misconceptions sorted by count/confidence/label | unit | `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py::test_cohort_summary_ranking_is_deterministic -q` | ✅ | ⬜ pending |
| 3-02-01 | 02 | 2 | RPT-02 | T-03-03 | `teacher_report.json` deterministic schema and ordering | integration | `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py::test_report_json_is_deterministic -q` | ✅ | ⬜ pending |
| 3-02-02 | 02 | 2 | RPT-04 | T-03-04 | Evidence snippets contain only question_text and student_answer | integration | `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py::test_evidence_snippets_are_concise_and_scoped -q` | ✅ | ⬜ pending |

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

**Approval:** planner-ready
