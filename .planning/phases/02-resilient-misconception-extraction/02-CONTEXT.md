# Phase 2: Resilient Misconception Extraction - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase builds reliable misconception extraction on top of Phase 1 incorrect-only rows: strict JSON prompt/response contracts, OpenRouter Qwen 3.6 invocation, timeout/retry resilience, malformed-JSON repair, and deterministic fallback output when the model path fails.

</domain>

<decisions>
## Implementation Decisions

### Prompt JSON contract
- **D-01:** Enforce JSON-only model responses using a fixed object schema (no prose, no markdown wrappers, no extra keys).
- **D-02:** Require typed fields that are directly machine-consumable for downstream aggregation: `student_id`, `concept`, `question_text`, `student_answer`, `misconceptions` (array), and per-misconception `label`, `rationale`, `confidence`.

### OpenRouter invocation profile
- **D-03:** Use OpenRouter with Qwen 3.6 free model route as the primary backend for this phase.
- **D-04:** Keep API key and model selection in environment configuration (`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`) and centralize HTTP client settings in one module.

### Retry and timeout policy
- **D-05:** Apply bounded retry behavior for transient failures (timeouts/service errors) with deterministic backoff.
- **D-06:** Use explicit request timeout budgets and stop after max retry count, returning structured failure metadata instead of crashing.

### Malformed JSON repair and deterministic fallback
- **D-07:** On malformed model output, run a single JSON-repair pass before giving up on the raw response.
- **D-08:** If repair still fails, run a deterministic keyword-based fallback analyzer and emit the same output schema shape.

### Execution granularity
- **D-09:** Process one incorrect submission per analysis call to keep failure isolation and traceability simple for prototype scope.
- **D-10:** Preserve stable input ordering and deterministic outputs for identical inputs/config.

### the agent's Discretion
- Exact backoff interval values and timeout constants, as long as behavior remains bounded and deterministic.
- Internal function names/module layout for prompt construction, API client, repair logic, and fallback analyzer.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and requirements
- `prd.md` - LLM module requirements, resilience expectations, and prototype constraints.
- `.planning/PROJECT.md` - active constraints, provider choice, and reliability priorities.
- `.planning/REQUIREMENTS.md` - Phase 2 requirement IDs `LLM-01` to `LLM-04`.
- `.planning/ROADMAP.md` - Phase 2 boundary and success criteria.

### Upstream data contracts
- `src/pipeline/ingest.py` - ingestion output contract and pipeline handoff behavior.
- `src/pipeline/filtering.py` - strict incorrect-only forwarding rules that define Phase 2 input set.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `run_ingestion_pipeline` in `src/pipeline/ingest.py` already returns normalized incorrect rows plus structured summary metadata.
- Current tests establish deterministic behavior patterns for malformed-row handling and strict boolean filtering.

### Established Patterns
- Fail-closed validation with explicit reason codes is already established and should continue in model/JSON failure paths.
- JSONL/JSON summary style diagnostics are already used; Phase 2 should keep machine-readable failure surfaces.

### Integration Points
- Phase 2 should consume the forwarded incorrect rows from `run_ingestion_pipeline` output.
- Phase 2 outputs must preserve deterministic structured fields that Phase 3 aggregation can consume without schema translation.

</code_context>

<specifics>
## Specific Ideas

- User requested low-chatter capture for this discussion: all identified gray areas were selected and resolved in one pass to reduce request overhead.
- Keep provider configuration substitution-friendly (env vars) and avoid hardcoding secrets or model settings in call sites.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope.

</deferred>

---

*Phase: 02-resilient-misconception-extraction*
*Context gathered: 2026-04-12*
