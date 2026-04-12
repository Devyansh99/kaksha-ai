# Phase 3: Teacher Report and Aggregation - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase converts Phase 2 analyzed misconception outputs into deterministic, teacher-facing report artifacts: per-student per-concept mastery scores, misconception evidence snippets, and cohort-level summary insights in `teacher_report.json`.

</domain>

<decisions>
## Implementation Decisions

### Mastery scoring policy
- **D-01:** Use misconception-severity deduction (confidence-weighted) as the Phase 3 scoring strategy.
- **D-02:** Compute a deterministic integer `mastery_score` in `[0, 100]` per `student_id + concept` by applying confidence-weighted penalties and clamping/rounding consistently.

### Deterministic report schema
- **D-03:** Keep output keyed by `student -> concept -> mastery_score + identified_misconceptions[]` and include cohort summary + metadata sections.
- **D-04:** Enforce deterministic serialization: stable sorting for students/concepts/misconception labels and stable JSON writing settings on every run.

### Cohort summary ranking
- **D-05:** For each concept, rank top misconceptions by occurrence count (descending), then average confidence (descending), then label (ascending).
- **D-06:** Include cohort summary metrics per misconception: `occurrences`, `affected_students`, and `avg_confidence`.

### Evidence snippet policy
- **D-07:** Include concise evidence snippets for each misconception using only `question_text` and `student_answer` fields.
- **D-08:** Limit to at most 3 evidence snippets per misconception per concept aggregate to keep report compact and teacher-readable.

### Failure-status handling
- **D-09:** Include analyzed rows with statuses `ok`, `json_repaired`, and `fallback_used` in aggregation.
- **D-10:** Exclude `retry_exhausted` rows from misconception evidence and mastery deduction, but report them in deterministic metadata counters.

### the agent's Discretion
- Exact helper/module split for aggregation utilities vs report writer.
- Exact clipping lengths for evidence snippet text, as long as snippets remain concise and deterministic.

</decisions>

<specifics>
## Specific Ideas

- Discussion executed in low-request mode: all relevant gray areas were selected and resolved in one pass to reduce interaction overhead.
- Keep report outputs deterministic enough for repeated test assertions and stable diffs.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and requirement contracts
- `prd.md` - aggregation goals, mastery scoring expectations, and required report artifact.
- `.planning/PROJECT.md` - current validated scope and output constraints.
- `.planning/REQUIREMENTS.md` - Phase 3 requirement IDs `RPT-01` to `RPT-04`.
- `.planning/ROADMAP.md` - Phase 3 boundary and success criteria.

### Upstream execution decisions and outputs
- `.planning/phases/02-resilient-misconception-extraction/02-CONTEXT.md` - locked extraction contract and status semantics.
- `.planning/phases/02-resilient-misconception-extraction/02-01-SUMMARY.md` - prompt/client contract outcomes feeding aggregation.
- `.planning/phases/02-resilient-misconception-extraction/02-02-SUMMARY.md` - resilience status behavior and fallback output guarantees.

### Source interfaces for aggregation input
- `src/pipeline/misconception_extractor.py` - analyzed row output shape and status/error metadata.
- `src/pipeline/json_resilience.py` - deterministic fallback misconception record structure.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `extract_for_incorrect_rows` in `src/pipeline/misconception_extractor.py` already yields stable row-level records for aggregation.
- `deterministic_keyword_fallback` in `src/pipeline/json_resilience.py` guarantees schema-compatible fallback entries.

### Established Patterns
- Deterministic reason/status fields are already used (`ok`, `json_repaired`, `fallback_used`, `retry_exhausted`) and should drive aggregation branch logic.
- Test-first pipeline style is established: requirement behavior is validated with explicit pytest functions and deterministic assertions.

### Integration Points
- Phase 3 should consume Phase 2 analyzed rows directly and produce `teacher_report.json` without schema translation layers.
- Phase 3 output schema must be deterministic to support Phase 4 quality enrichment and comparisons.

</code_context>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope.

</deferred>

---

*Phase: 03-teacher-report-and-aggregation*
*Context gathered: 2026-04-12*
