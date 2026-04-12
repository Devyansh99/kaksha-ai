# Requirements: Misconception Analyzer Pipeline

**Defined:** 2026-04-12
**Core Value:** Teachers get clear, per-student and per-concept misconception insights in a valid JSON report they can act on.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Data Ingestion

- [x] **DATA-01**: User can run ingestion that validates required schema fields for each log row
- [x] **DATA-02**: User can run cleaning that normalizes timestamps into a consistent parseable format
- [x] **DATA-03**: User can see malformed rows dropped with explicit reason logging
- [x] **DATA-04**: User can process only incorrect submissions for misconception analysis

### Misconception Analysis

- [x] **LLM-01**: User can generate strict JSON-only LLM prompts for each incorrect submission
- [x] **LLM-02**: User can run misconception analysis through OpenRouter Qwen 3.6 free model using env-var API key config
- [x] **LLM-03**: User can recover from timeout/service errors through bounded retries and error handling
- [x] **LLM-04**: User can recover from malformed model JSON via repair attempt then deterministic fallback analyzer

### Aggregation and Reporting

- [x] **RPT-01**: User can compute mastery score (0-100) per student per concept
- [x] **RPT-02**: User can produce `teacher_report.json` with deterministic schema
- [x] **RPT-03**: User can view cohort-level concept summary of top misconceptions
- [x] **RPT-04**: User can view concise evidence snippets (`question_text`, `student_answer`) for each misconception finding

### Quality Enhancements

- [x] **QLT-01**: User can normalize free-text misconception labels to a fixed taxonomy
- [x] **QLT-02**: User can compare two prompting strategies and record a short A/B result summary
- [x] **QLT-03**: User can view a confidence score per identified misconception

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Platform and Scale

- **PLAT-01**: User can review results in a teacher dashboard UI
- **PLAT-02**: User can ingest near real-time student log streams
- **PLAT-03**: User can run with multi-tenant auth and role-based access controls
- **PLAT-04**: User can train/customize misconception classifiers with a dedicated ML pipeline

## Out of Scope

Explicitly excluded for this milestone.

| Feature | Reason |
|---------|--------|
| Full teacher dashboard UI | JSON output is the required prototype deliverable and UI would expand scope significantly |
| Real-time streaming ingestion | Batch file ingestion is sufficient for this prototype and timeline |
| Custom model training stack | Not needed to validate core value in a 4-hour prototype |
| Enterprise auth/roles and hardening | Prototype is local/demo focused, not production deployment |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Complete |
| DATA-02 | Phase 1 | Complete |
| DATA-03 | Phase 1 | Complete |
| DATA-04 | Phase 1 | Complete |
| LLM-01 | Phase 2 | Complete |
| LLM-02 | Phase 2 | Complete |
| LLM-03 | Phase 2 | Complete |
| LLM-04 | Phase 2 | Complete |
| RPT-01 | Phase 3 | Complete |
| RPT-02 | Phase 3 | Complete |
| RPT-03 | Phase 3 | Complete |
| RPT-04 | Phase 3 | Complete |
| QLT-01 | Phase 4 | Complete |
| QLT-02 | Phase 4 | Complete |
| QLT-03 | Phase 4 | Complete |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-04-12*
*Last updated: 2026-04-12 after Phase 3 completion updates*
