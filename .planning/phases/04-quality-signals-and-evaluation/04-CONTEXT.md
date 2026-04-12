# Phase 4: Quality Signals and Evaluation - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase improves quality trust signals for misconception outputs by adding deterministic label normalization to a fixed taxonomy, confidence visibility enhancements, and a short A/B prompt strategy comparison summary.

</domain>

<decisions>
## Implementation Decisions

### Taxonomy design scope
- **D-01:** Use a fixed, versioned taxonomy with stable canonical labels and groups so normalized outputs are deterministic across runs.
- **D-02:** Keep both `raw_label` (original extracted label) and normalized fields (`normalized_label`, `taxonomy_group`) in quality outputs for traceability.

### Normalization method policy
- **D-03:** Use deterministic, rule-first normalization only (exact match -> lowercase-normalized exact match -> alias/keyword rules), with no additional model call in this phase.
- **D-04:** If no taxonomy match exists, map to `Uncategorized` and add a deterministic reason marker (`no_taxonomy_match`) instead of dropping the item.

### Prompt strategy A/B comparison
- **D-05:** Compare two strategies on the same input slice: strict JSON zero-shot vs strict JSON few-shot.
- **D-06:** Record a short deterministic comparison summary using these metrics in priority order: parse success rate, normalized-label coverage, consistency across reruns, then average confidence.

### Confidence visibility policy
- **D-07:** Preserve numeric confidence in `[0,1]` (rounded to 2 decimals) and add confidence bands: `low` (<0.40), `medium` (0.40-0.74), `high` (>=0.75).
- **D-08:** For aggregated confidence signals, compute from included statuses (`ok`, `json_repaired`, `fallback_used`) and exclude `retry_exhausted` from confidence math while still counting it in metadata.

### the agent's Discretion
- Initial taxonomy category names and alias dictionaries can be tuned for clarity as long as mappings remain deterministic.
- A/B sample size can default to all available incorrect rows when small, or a fixed deterministic subset when larger.

</decisions>

<specifics>
## Specific Ideas

- User direction for this discussion: apply best-practice defaults across all remaining gray areas.
- Keep outputs terminal/pipeline friendly (JSON + concise markdown summary artifacts), not UI/dashboard-specific.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and phase scope
- `prd.md` - core project goal, module-level expectations, and explicit requirement for prompt strategy comparison.
- `.planning/PROJECT.md` - validated project constraints and active Phase 4 focus.
- `.planning/REQUIREMENTS.md` - Phase 4 requirement IDs `QLT-01`, `QLT-02`, `QLT-03`.
- `.planning/ROADMAP.md` - Phase 4 goal and success criteria contract.

### Prior phase decisions and outputs
- `.planning/phases/03-teacher-report-and-aggregation/03-CONTEXT.md` - locked deterministic report and status-handling decisions.
- `.planning/phases/03-teacher-report-and-aggregation/03-01-SUMMARY.md` - aggregation behavior implemented for RPT-01/RPT-03.
- `.planning/phases/03-teacher-report-and-aggregation/03-02-SUMMARY.md` - report assembly and evidence behavior implemented for RPT-02/RPT-04.

### Existing code contracts
- `src/pipeline/misconception_prompt.py` - strict JSON prompt contract and output key expectations.
- `src/pipeline/misconception_extractor.py` - extraction orchestration and status semantics.
- `src/pipeline/report_aggregation.py` - deterministic ranking and confidence handling primitives.
- `src/pipeline/report_pipeline.py` - teacher report construction and status-filtered evidence behavior.
- `tests/test_resilient_misconception_extraction.py` - current reliability/contract verification.
- `tests/test_teacher_report_aggregation.py` - current deterministic report assertions to extend in this phase.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `INCLUDED_STATUSES` and confidence clamping helpers in `src/pipeline/report_aggregation.py` can be reused for quality-signal calculations.
- `build_teacher_report` in `src/pipeline/report_pipeline.py` is the integration point for adding normalized labels and confidence bands.
- Existing resilient extraction path in `src/pipeline/misconception_extractor.py` already emits deterministic statuses suitable for quality filtering.

### Established Patterns
- Deterministic ordering and deterministic JSON serialization are already locked and should be preserved.
- Retry-exhausted rows are tracked in metadata but excluded from instructional signal math.
- Test-first pattern with narrow pytest cases is already established for each requirement.

### Integration Points
- Quality normalization should run after misconception extraction and before/within final report assembly.
- A/B strategy comparison should produce a compact artifact tied to phase outputs, then feed next planning/verification steps.

</code_context>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope.

</deferred>

---

*Phase: 04-quality-signals-and-evaluation*
*Context gathered: 2026-04-12*
