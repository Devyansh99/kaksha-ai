---
phase: 03-teacher-report-and-aggregation
status: complete
source: gsd-plan-phase
created: 2026-04-12
---

# Phase 3 Research: Teacher Report and Aggregation

## Objective

Research implementation approach for deterministic teacher-facing aggregation from Phase 2 misconception outputs, including mastery scoring, cohort summaries, and report serialization.

## Inputs Reviewed

- `.planning/phases/03-teacher-report-and-aggregation/03-CONTEXT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `src/pipeline/misconception_extractor.py`
- `src/pipeline/json_resilience.py`
- `.planning/phases/02-resilient-misconception-extraction/02-01-SUMMARY.md`
- `.planning/phases/02-resilient-misconception-extraction/02-02-SUMMARY.md`
- `prd.md`

## Recommended Technical Approach

1. Build aggregation from normalized row records emitted by Phase 2 (`student_id`, `concept`, `misconceptions`, `status`, `error_code`).
2. Compute mastery per `student_id + concept` using confidence-weighted misconception penalties with deterministic clamping to integer `[0, 100]`.
3. Build cohort concept summaries by grouping misconception labels and ranking by occurrence count, then average confidence, then label.
4. Collect concise evidence snippets (`question_text`, `student_answer`) and cap to 3 per misconception aggregate.
5. Exclude `retry_exhausted` rows from misconception evidence/scoring while exposing deterministic metadata counters in report output.
6. Serialize `teacher_report.json` with deterministic ordering and stable JSON writer options.

## Input Contract from Phase 2

Expected analyzed row shape:

- `student_id` (string)
- `concept` (string)
- `question_text` (string)
- `student_answer` (string)
- `misconceptions` (array of `{label, rationale, confidence}`)
- `source` (`llm` | `fallback`)
- `status` (`ok` | `json_repaired` | `fallback_used` | `retry_exhausted`)
- `error_code` (nullable string)

## Report Contract for Phase 3

### Per-student section

`student -> concept -> {
  mastery_score,
  identified_misconceptions: [{label, rationale, confidence, evidence_snippets[]}]
}`

### Cohort section

`cohort_summary -> concept -> top_misconceptions: [{label, occurrences, affected_students, avg_confidence, evidence_snippets[]}]`

### Metadata section

- `total_rows_processed`
- `rows_included`
- `rows_excluded_retry_exhausted`
- `generated_at` (deterministic source or controlled timestamp injection in tests)

## Risks and Mitigations

- Risk: nondeterministic ordering causes unstable `teacher_report.json` diffs.
  - Mitigation: explicit sort order for students, concepts, labels, and evidence snippets.
- Risk: retry-exhausted rows pollute instructional insight quality.
  - Mitigation: exclude from scoring/evidence and track in metadata counters.
- Risk: overly verbose evidence reduces teacher usability.
  - Mitigation: concise snippet policy with deterministic maximum count.

## Validation Architecture

- Quick test command: `venv\Scripts\python -m pytest tests/test_teacher_report_aggregation.py -q`
- Full test command: `venv\Scripts\python -m pytest -q`
- Required checks in this phase:
  - mastery score calculations are deterministic and bounded (`RPT-01`)
  - report JSON structure is deterministic and stable across reruns (`RPT-02`)
  - cohort misconception ranking follows fixed tie-break rules (`RPT-03`)
  - evidence snippets include `question_text` and `student_answer` only (`RPT-04`)

## Validation Architecture

Phase includes deterministic scoring and serialization logic with explicit output contract checks suitable for Nyquist validation strategy generation.

## Output

Research complete; ready for plan generation and verification.
