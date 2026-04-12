---
phase: 01-data-contracts-and-cleaning
status: complete
source: gsd-plan-phase
created: 2026-04-12
---

# Phase 1 Research: Data Contracts and Cleaning

## Objective

Research implementation approach for strict ingestion contracts, timestamp normalization, malformed-row handling, and incorrect-attempt filtering for `student_logs.json`.

## Inputs Reviewed

- `.planning/phases/01-data-contracts-and-cleaning/01-CONTEXT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/STATE.md`
- `prd.md`

## Recommended Technical Approach

1. Use a pandas-first pipeline with explicit schema validation prior to any transform.
2. Encode required-column contract in a single source-of-truth constant and validate row-level null/type rules.
3. Normalize timestamps with strict parser flow: parse known formats, convert to UTC, serialize as ISO-8601.
4. Treat invalid or missing `is_correct` as malformed; forward only strict `False` rows to downstream analysis.
5. Emit both console summary and machine-readable drop log artifact (`artifacts/drop_log.jsonl`).

## Data Contract Details

### Required fields

`student_id`, `subject`, `concept`, `question_text`, `correct_answer`, `student_answer`, `is_correct`, `timestamp`

### Drop reason code set

- `missing_required_field`
- `invalid_field_type`
- `invalid_timestamp`
- `invalid_is_correct`

## Suggested File Layout for Execution

- `src/pipeline/contracts.py` — required schema definitions and validators
- `src/pipeline/cleaning.py` — row cleaning and timestamp normalization
- `src/pipeline/filtering.py` — incorrect-attempt filtering rules
- `src/pipeline/drop_log.py` — structured drop log writer + summary counters
- `src/pipeline/ingest.py` — orchestration entry for phase output contract
- `tests/test_data_contracts_and_cleaning.py` — automated checks for DATA-01..DATA-04

## Risks and Mitigations

- Risk: permissive parsing can leak malformed data downstream.
  - Mitigation: fail-closed row policy with explicit reason codes.
- Risk: timezone ambiguity affects ordering and scoring in later phases.
  - Mitigation: normalize all accepted timestamps to UTC ISO-8601.
- Risk: silent fallback behavior for `is_correct` creates false misconceptions.
  - Mitigation: strict boolean validation; drop unknowns.

## Validation Architecture

- Quick test command: `venv\Scripts\python -m pytest tests/test_data_contracts_and_cleaning.py -q`
- Full test command: `venv\Scripts\python -m pytest -q`
- Required checks in this phase:
  - schema enforcement drops malformed rows with reason codes
  - timestamp normalization emits UTC ISO strings
  - filtering forwards only rows with `is_correct == False`
  - structured drop-log file is generated with per-row metadata

## Output

Research complete; ready for planning and validation-strategy generation.
