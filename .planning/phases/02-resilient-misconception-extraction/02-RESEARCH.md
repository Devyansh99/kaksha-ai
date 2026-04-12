---
phase: 02-resilient-misconception-extraction
status: complete
source: gsd-plan-phase
created: 2026-04-12
---

# Phase 2 Research: Resilient Misconception Extraction

## Objective

Research implementation approach for strict JSON misconception extraction using OpenRouter Qwen 3.6 with bounded retry, malformed-JSON repair, and deterministic fallback behavior.

## Inputs Reviewed

- `.planning/phases/02-resilient-misconception-extraction/02-CONTEXT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `src/pipeline/ingest.py`
- `src/pipeline/filtering.py`
- `prd.md`

## Recommended Technical Approach

1. Define an explicit response contract and prompt builder that demand JSON-only output with no prose wrappers.
2. Implement a centralized OpenRouter client module that reads `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` from environment variables.
3. Enforce deterministic network resilience: fixed timeout budget, bounded retries, deterministic backoff schedule.
4. Implement malformed-JSON handling as one repair attempt followed by deterministic fallback analyzer if still invalid.
5. Keep extraction deterministic and traceable by processing one incorrect submission at a time in stable input order.

## Response Contract

### Top-level fields

- `student_id` (string)
- `concept` (string)
- `question_text` (string)
- `student_answer` (string)
- `misconceptions` (array)

### Misconception item fields

- `label` (string)
- `rationale` (string)
- `confidence` (number in [0, 1])

### Failure metadata fields (resilience path)

- `source` (`llm` | `fallback`)
- `status` (`ok` | `retry_exhausted` | `json_repaired` | `fallback_used`)
- `error_code` (nullable string)

## Suggested File Layout for Execution

- `src/pipeline/misconception_prompt.py` - strict prompt builder and schema contract helpers
- `src/pipeline/openrouter_client.py` - centralized OpenRouter call path with timeout/retry behavior
- `src/pipeline/json_resilience.py` - JSON parsing, one-pass repair, fallback trigger logic
- `src/pipeline/misconception_extractor.py` - per-row extraction orchestrator over incorrect rows
- `tests/test_resilient_misconception_extraction.py` - automated checks for LLM-01 to LLM-04

## Risks and Mitigations

- Risk: model returns prose or malformed JSON.
  - Mitigation: strict prompt contract, one repair pass, then deterministic fallback output.
- Risk: intermittent OpenRouter errors/timeouts cause pipeline crashes.
  - Mitigation: bounded retries with deterministic backoff and structured failure status.
- Risk: hidden nondeterminism creates unstable downstream reporting.
  - Mitigation: one-row processing order, fixed response contract, stable fallback behavior.

## Validation Architecture

- Quick test command: `venv\Scripts\python -m pytest tests/test_resilient_misconception_extraction.py -q`
- Full test command: `venv\Scripts\python -m pytest -q`
- Required checks in this phase:
  - prompt requires JSON-only contract fields (`LLM-01`)
  - OpenRouter config is env-var driven and centralized (`LLM-02`)
  - retry/timeout path is bounded and non-crashing (`LLM-03`)
  - malformed JSON triggers repair then deterministic fallback (`LLM-04`)

## Output

Research complete; ready for planning and validation-strategy generation.
