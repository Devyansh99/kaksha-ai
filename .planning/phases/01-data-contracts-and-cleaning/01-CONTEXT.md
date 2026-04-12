# Phase 1: Data Contracts and Cleaning - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase defines robust ingestion contracts for `student_logs.json`: enforce schema validity, normalize timestamps, log malformed drops, and pass forward only incorrect submissions for downstream misconception analysis.

</domain>

<decisions>
## Implementation Decisions

### Schema contract and malformed policy
- **D-01:** Enforce strict required fields per row: `student_id`, `subject`, `concept`, `question_text`, `correct_answer`, `student_answer`, `is_correct`, `timestamp`.
- **D-02:** Drop rows when any required field is missing or invalid for contract checks, and log a reason code for each drop.

### Timestamp normalization policy
- **D-03:** Parse common ISO/date-like timestamp formats and normalize successful parses to UTC ISO-8601.
- **D-04:** Treat unparseable timestamps as malformed rows and drop them with explicit logging.

### Incorrect-attempt filtering rules
- **D-05:** Accept only strict boolean values for `is_correct`; non-boolean or missing values are malformed and dropped.
- **D-06:** Forward only rows where `is_correct == false` to the misconception analysis stage.

### Drop logging output format
- **D-07:** Emit a console summary of total rows, valid rows, dropped rows, and drop reason counts.
- **D-08:** Emit a structured drop-log artifact (JSON/JSONL) with per-row reason metadata for audit/debugging.

### the agent's Discretion
- Choose concrete parser utilities and dataframe implementation details while preserving all locked decisions above.
- Choose exact structured log filename/location and reason-code schema naming.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and phase scope
- `prd.md` — Original product requirements and success criteria for ingestion quality.
- `.planning/PROJECT.md` — Project constraints, core value, and locked high-level decisions.
- `.planning/ROADMAP.md` — Phase boundary and required success criteria for Phase 1.

### Requirement contracts
- `.planning/REQUIREMENTS.md` — Phase-mapped requirement IDs (`DATA-01` to `DATA-04`) and traceability.

### Research context
- `.planning/research/SUMMARY.md` — Recommended architecture/build-order implications for data-contract-first implementation.
- `.planning/research/STACK.md` — Prototype stack constraints and implementation guidance.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No existing source modules were found yet for ingestion/cleaning logic; Phase 1 will establish initial project code structure.
- Existing planning artifacts define requirements and constraints that should be treated as implementation contracts.

### Established Patterns
- Documentation-first GSD flow is active (`PROJECT.md` -> `REQUIREMENTS.md` -> `ROADMAP.md` -> phase context).
- Project currently expects local development execution and deterministic JSON artifacts.

### Integration Points
- Phase 1 outputs become direct inputs for Phase 2 (`LLM-01` to `LLM-04`): cleaned/normalized incorrect submissions and structured drop logs.
- Output data contract should be stable so aggregation/reporting phases can consume without schema drift.

</code_context>

<specifics>
## Specific Ideas

No additional specific requirements beyond locked decisions; standard robust data-pipeline practices are acceptable within the phase boundary.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-data-contracts-and-cleaning*
*Context gathered: 2026-04-12*
