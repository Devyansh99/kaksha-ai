# Requirements: Misconception Analyzer Pipeline

**Defined:** 2026-04-12
**Core Value:** Teachers get clear, per-student and per-concept misconception insights in a valid JSON report they can act on.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Data Ingestion

- [ ] **DATA-01**: User can run ingestion that validates required schema fields for each log row
- [ ] **DATA-02**: User can run cleaning that normalizes timestamps into a consistent parseable format
- [ ] **DATA-03**: User can see malformed rows dropped with explicit reason logging
- [ ] **DATA-04**: User can process only incorrect submissions for misconception analysis

### Misconception Analysis

- [ ] **LLM-01**: User can generate strict JSON-only LLM prompts for each incorrect submission
- [ ] **LLM-02**: User can run misconception analysis through OpenRouter Qwen 3.6 free model using env-var API key config
- [ ] **LLM-03**: User can recover from timeout/service errors through bounded retries and error handling
- [ ] **LLM-04**: User can recover from malformed model JSON via repair attempt then deterministic fallback analyzer

### Aggregation and Reporting

- [ ] **RPT-01**: User can compute mastery score (0-100) per student per concept
- [ ] **RPT-02**: User can produce `teacher_report.json` with deterministic schema
- [ ] **RPT-03**: User can view cohort-level concept summary of top misconceptions
- [ ] **RPT-04**: User can view concise evidence snippets (`question_text`, `student_answer`) for each misconception finding

### Quality Enhancements

- [ ] **QLT-01**: User can normalize free-text misconception labels to a fixed taxonomy
- [ ] **QLT-02**: User can compare two prompting strategies and record a short A/B result summary
- [ ] **QLT-03**: User can view a confidence score per identified misconception

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
| DATA-01 | TBD | Pending |
| DATA-02 | TBD | Pending |
| DATA-03 | TBD | Pending |
| DATA-04 | TBD | Pending |
| LLM-01 | TBD | Pending |
| LLM-02 | TBD | Pending |
| LLM-03 | TBD | Pending |
| LLM-04 | TBD | Pending |
| RPT-01 | TBD | Pending |
| RPT-02 | TBD | Pending |
| RPT-03 | TBD | Pending |
| RPT-04 | TBD | Pending |
| QLT-01 | TBD | Pending |
| QLT-02 | TBD | Pending |
| QLT-03 | TBD | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 0
- Unmapped: 15

---
*Requirements defined: 2026-04-12*
*Last updated: 2026-04-12 after initial definition*
