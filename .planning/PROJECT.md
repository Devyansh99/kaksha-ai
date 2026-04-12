# Misconception Analyzer Pipeline

## What This Is

A lightweight Python pipeline that analyzes student Q&A logs to detect specific misconceptions and produce a teacher-facing aggregate report. It is intended as an AI Engineer Intern prototype for kaksha.ai Summer 2026. The pipeline prioritizes robust data cleaning, structured LLM outputs, and reliable fallback behavior.

## Core Value

Teachers get clear, per-student and per-concept misconception insights in a valid JSON report they can act on.

## Requirements

### Validated

- ✓ Ingestion enforces schema validation, timestamp normalization, malformed-drop logging, and strict incorrect-only forwarding — Phase 1 (2026-04-12)

### Active

- [ ] Identify misconceptions from incorrect answers with strict JSON-only LLM outputs and resilient failure handling
- [ ] Generate `teacher_report.json` keyed by student and concept with mastery score plus identified misconceptions

### Out of Scope

- Production-scale deployment and MLOps hardening — prototype scope is limited to local/demo execution
- Full teacher dashboard UI — deliverable is JSON output, not a frontend application

## Context

- Internship prototype target effort is about 4 hours
- Input schema includes: student_id, subject, concept, question_text, correct_answer, student_answer, is_correct, timestamp
- Dataset must include at least 10 records with 1-2 intentionally malformed rows
- LLM analysis includes prompt builder, backend integration, and resilience for timeout/error/malformed JSON
- Optional bonus includes comparing two prompting strategies

## Constraints

- **Timeline**: ~4 hours — must keep implementation lightweight and focused
- **Output Format**: `teacher_report.json` — required deliverable format
- **LLM Provider**: OpenRouter Qwen 3.6 free model — Gemini daily API request quota is exhausted today
- **Reliability**: Pipeline must not crash on malformed data or LLM failures

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use OpenRouter Qwen 3.6 free model instead of Gemini/Ollama | Gemini daily quota is exhausted; cloud free model keeps project moving without local LLM setup | — Pending |
| Keep keyword-based mock as fallback path | Guarantees end-to-end run even when API access is unavailable | — Pending |
| Use per-student per-concept mastery scoring in `teacher_report.json` | Matches reporting goal and success criteria in PRD | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check -> still the right priority?
3. Audit Out of Scope -> reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-12 after Phase 1 completion*
