# Project Research Summary

**Project:** Misconception Analyzer Pipeline
**Domain:** Educational learning-analytics pipeline (LLM-assisted misconception detection)
**Researched:** 2026-04-12
**Confidence:** MEDIUM

## Executive Summary

This is a teacher-facing analytics pipeline, not a general AI app. The proven pattern is a linear, contract-first data workflow: clean logs, analyze only incorrect attempts, enforce strict JSON output from the model, aggregate to student/concept mastery, and emit a deterministic report. For this project scope (local prototype, short build window), experts prioritize reliability and output quality over infrastructure depth.

The recommended approach is Python 3.12 with a small stack (`pandas`, `pydantic`, OpenAI SDK against OpenRouter, retries via `tenacity`) and a fallback analyzer so the run never fails on model/API issues. Main risks are contract breakage (non-JSON model output), false pedagogy signals (every wrong answer labeled as misconception), and aggregation distortion (timestamp/taxonomy/duplicate issues). Mitigation is strict schema validation, explicit non-conceptual class handling, canonical concept mapping, dedup keys, and fallback-rate quality gates.

## Key Findings

### Recommended Stack

Use a minimal, prototype-first stack that emphasizes deterministic behavior.

**Core technologies:**
- Python 3.12 + `venv`: fast local setup with strong library compatibility.
- `pandas` + `pydantic`: robust cleaning plus strict contracts for pipeline I/O.
- OpenAI Python SDK with OpenRouter base URL: fastest stable path to call Qwen free model.
- `tenacity` + `python-dotenv`: resilient retries/timeouts and clean secret management.
- `pytest` + `ruff`: quick confidence and hygiene for a small codebase.

### Expected Features

**Must have (table stakes):**
- Input validation and malformed-row drop logging.
- Incorrect-attempt filtering before misconception analysis.
- Strict JSON-only model output contract with parser validation.
- Retry/repair/fallback flow so one bad response does not fail the run.
- Per-student, per-concept mastery + `teacher_report.json` output.

**Should have (differentiators):**
- Canonical misconception taxonomy normalization (small fixed label set).
- Confidence score and evidence snippets (`question_text`, `student_answer`).
- Concept-level cohort summary for class-wide intervention planning.

**Defer (v2+):**
- Dashboard UI, real-time ingestion, custom model training, multi-tenant security scope.

### Architecture Approach

Build a one-way, single-process pipeline with pure-function modules where possible.

**Major components:**
1. Ingest + validate/clean: normalize schema, timestamps, concept aliases, and log dropped rows.
2. Misconception analysis path: prompt builder -> LLM client -> strict parser -> fallback analyzer.
3. Aggregation + report writer: compute mastery and misconception summaries, then write deterministic JSON.

**Recommended build order:**
1. Freeze report/data contracts.
2. Implement ingest/clean/drop-log.
3. Implement aggregation/report with mock misconceptions.
4. Add LLM strict JSON path.
5. Add fallback routing and end-to-end smoke test.

### Critical Pitfalls

1. **Prompt label leakage** - keep diagnosis grounded in student response evidence, not answer-key cues.
2. **Free-form model output** - enforce schema, bounded repair retries, then deterministic fallback.
3. **Wrong != misconception** - include explicit non-conceptual/insufficient-evidence class.
4. **Timestamp/taxonomy drift** - normalize time and concept labels before scoring.
5. **Silent fallback overuse** - track fallback ratio and quality-gate when threshold is exceeded.

## Implications for Roadmap

### Phase 1: Data Contracts and Cleaning Foundation
**Rationale:** All downstream quality depends on clean, canonical, deduplicated records.
**Delivers:** Input schema, cleaner, malformed-row logs, timestamp normalization, concept alias map.
**Addresses:** Core reliability features and ingestion table stakes.
**Avoids:** Timestamp distortion, taxonomy drift, duplicate-count inflation.

### Phase 2: Misconception Extraction Engine
**Rationale:** This is the highest uncertainty and highest value area.
**Delivers:** Prompt contract, OpenRouter integration, strict parser, retry/repair, fallback analyzer.
**Uses:** OpenAI SDK, `tenacity`, `pydantic` validation.
**Avoids:** JSON contract breaks, leakage, over-labeling, unsafe labels.

### Phase 3: Aggregation, Scoring, and Teacher Report
**Rationale:** Converts row-level outputs into educator-actionable artifacts.
**Delivers:** Student/concept mastery, misconception summaries, cohort-level view, report writer.
**Implements:** Deterministic grouping, stable sorting, schema-validated final output.

### Phase 4: Evaluation and Guardrails
**Rationale:** Prevents hidden quality regressions before expanding scope.
**Delivers:** Fixed benchmark fixture, fallback-ratio gate, sample teacher-review checks.
**Avoids:** "Pipeline succeeds but insights degrade" failure mode.

### Roadmap Implementation Guidance

- Plan Phase 2 with explicit risk controls first-class, not as cleanup tasks.
- Keep each phase acceptance criteria contract-based (input schema, response schema, report schema).
- Add one differentiator only (taxonomy normalization) in MVP; defer the rest to protect timeline.
- Add quality telemetry early (`rows_dropped`, `llm_failures`, `fallback_used`) to support phase-gate decisions.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** model prompt contract and misconception ontology calibration for educational validity.
- **Phase 4:** evaluation rubric design and fallback quality thresholds.

Phases with standard patterns (skip deep research):
- **Phase 1:** data validation/cleaning and logging are well-established patterns.
- **Phase 3:** deterministic aggregation/reporting is straightforward once contracts are fixed.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based on current official docs and common Python pipeline practice. |
| Features | MEDIUM | Strong pattern fit, but final prioritization depends on teacher feedback. |
| Architecture | HIGH | Clear, low-risk batch architecture for prototype scope. |
| Pitfalls | MEDIUM | Risks are credible; severity thresholds should be validated on real data. |

**Overall confidence:** MEDIUM

### Gaps to Address

- Misconception taxonomy calibration with actual classroom examples.
- Threshold definitions for fallback-rate alarms and confidence score interpretation.
- Validation of mastery formula against teacher expectations before scaling feature scope.

## Sources

### Primary (HIGH confidence)
- Python docs (runtime compatibility and release lines)
- OpenRouter quickstart and OpenAI-compatible API docs
- OpenAI Python SDK, pandas, pydantic, tenacity, pytest, ruff package/documentation pages

### Secondary (MEDIUM confidence)
- Internal research synthesis in [STACK.md](.planning/research/STACK.md), [FEATURES.md](.planning/research/FEATURES.md), [ARCHITECTURE.md](.planning/research/ARCHITECTURE.md), and [PITFALLS.md](.planning/research/PITFALLS.md)

---
*Research completed: 2026-04-12*
*Ready for roadmap: yes*
