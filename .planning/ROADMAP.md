# Roadmap: Misconception Analyzer Pipeline

## Overview

This roadmap delivers a reliable prototype pipeline in four practical phases: establish clean data contracts, run resilient misconception extraction, aggregate teacher-facing insights, and harden quality signals for classroom usefulness.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Data Contracts and Cleaning** - Build robust ingestion, schema validation, normalization, and incorrect-row filtering.
 (completed 2026-04-12)
- [x] **Phase 2: Resilient Misconception Extraction** - Detect misconceptions through strict JSON LLM flows with retry/repair/fallback resilience.
 (completed 2026-04-12)
- [x] **Phase 3: Teacher Report and Aggregation** - Convert analyzed rows into mastery metrics and deterministic teacher report outputs.
 (completed 2026-04-12)
- [x] **Phase 4: Quality Signals and Evaluation** - Improve output quality through taxonomy normalization, confidence scoring, and prompt strategy comparison.
 (completed 2026-04-12)

## Phase Details

### Phase 1: Data Contracts and Cleaning
**Goal**: Users can ingest student logs into a validated, normalized dataset that is safe for downstream misconception analysis.
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04
**Success Criteria** (what must be TRUE):
  1. User can run ingestion that enforces required schema fields on every record.
  2. User can run cleaning that outputs consistently parseable timestamps across records.
  3. User can review malformed rows that were dropped with explicit reason logging.
  4. User can confirm that only incorrect submissions are passed forward for misconception analysis.
**Plans**: 2 plans
Plans:
- [x] 01-01-PLAN.md - contract validation and timestamp normalization foundation
- [x] 01-02-PLAN.md - incorrect-attempt filtering and structured drop logging integration
**UI hint**: no

### Phase 2: Resilient Misconception Extraction
**Goal**: Users can obtain misconception detections from incorrect submissions even when model responses or API calls fail intermittently.
**Depends on**: Phase 1
**Requirements**: LLM-01, LLM-02, LLM-03, LLM-04
**Success Criteria** (what must be TRUE):
  1. User can generate strict JSON-only prompts for each incorrect submission.
  2. User can execute analysis against OpenRouter Qwen 3.6 using env-var API key configuration.
  3. User can observe bounded retry behavior on timeout or service errors without pipeline crashes.
  4. User can still receive analyzable output when malformed model JSON triggers repair then deterministic fallback.
**Plans**: 2 plans
Plans:
- [x] 02-01-PLAN.md - strict JSON prompt contract and centralized OpenRouter client foundation
- [x] 02-02-PLAN.md - bounded retry, JSON repair, and deterministic fallback extraction orchestration
**UI hint**: no

### Phase 3: Teacher Report and Aggregation
**Goal**: Users can receive deterministic, actionable teacher-facing outputs from analyzed misconception results.
**Depends on**: Phase 2
**Requirements**: RPT-01, RPT-02, RPT-03, RPT-04
**Success Criteria** (what must be TRUE):
  1. User can view mastery scores from 0-100 for each student and concept.
  2. User can generate a deterministic `teacher_report.json` structure on repeated runs.
  3. User can review cohort-level concept summaries showing top misconceptions.
  4. User can inspect concise evidence snippets (`question_text`, `student_answer`) attached to findings.
**Plans**: 2 plans
Plans:
- [x] 03-01-PLAN.md - deterministic mastery scoring and cohort ranking aggregation core
- [x] 03-02-PLAN.md - deterministic report assembly, writer output, and evidence snippet projection
**UI hint**: no

### Phase 4: Quality Signals and Evaluation
**Goal**: Users can trust misconception outputs more through normalized labels, confidence visibility, and strategy comparison evidence.
**Depends on**: Phase 3
**Requirements**: QLT-01, QLT-02, QLT-03
**Success Criteria** (what must be TRUE):
  1. User can see free-text misconception labels normalized to a fixed taxonomy.
  2. User can compare two prompting strategies and review a short recorded A/B result summary.
  3. User can view a confidence score for each identified misconception in outputs.
**Plans**: 2 plans
Plans:
- [x] 04-01-PLAN.md - deterministic taxonomy normalization and confidence visibility in report outputs
- [x] 04-02-PLAN.md - deterministic prompt strategy comparison and A/B evidence summary generation
**UI hint**: no

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 1.1 -> 2 -> 2.1 -> 3 -> 3.1 -> 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Data Contracts and Cleaning | 2/2 | Complete    | 2026-04-12 |
| 2. Resilient Misconception Extraction | 2/2 | Complete    | 2026-04-12 |
| 3. Teacher Report and Aggregation | 2/2 | Complete    | 2026-04-12 |
| 4. Quality Signals and Evaluation | 2/2 | Complete    | 2026-04-12 |
