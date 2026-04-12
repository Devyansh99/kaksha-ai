# Phase 2: Resilient Misconception Extraction - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves alternatives considered.

**Date:** 2026-04-12
**Phase:** 02-resilient-misconception-extraction
**Areas discussed:** Prompt JSON contract, OpenRouter invocation profile, Retry and timeout policy, Malformed JSON repair and deterministic fallback, Execution granularity

---

## Prompt JSON contract

| Option | Description | Selected |
|--------|-------------|----------|
| Loose free-text with parser cleanup | Faster to prototype but fragile and non-deterministic for downstream parsing | |
| Single strict JSON object with fixed keys and typed fields only | Deterministic and planner-friendly contract for extraction and aggregation | ✓ |
| Mixed JSON plus explanation | Human-readable but violates strict-machine contract requirement | |

**User's choice:** Single strict JSON object with fixed keys and typed fields only
**Notes:** Auto-selected recommended default after user requested low-request-cost, one-pass discussion.

---

## OpenRouter invocation profile

| Option | Description | Selected |
|--------|-------------|----------|
| Hardcode model/client values in call sites | Quick but brittle and hard to rotate | |
| OpenRouter key and model from env vars with one centralized client config | Clear substitution path and consistent configuration | ✓ |
| Per-call ad-hoc config | Flexible but inconsistent and error-prone | |

**User's choice:** OpenRouter key and model from env vars with one centralized client config
**Notes:** Aligns with existing project constraints and prior decision to keep cloud model configurable.

---

## Retry and timeout policy

| Option | Description | Selected |
|--------|-------------|----------|
| Infinite retries until success | Maximizes eventual success but can hang pipeline | |
| No retries | Simpler but too brittle for intermittent provider failures | |
| Bounded retries with deterministic backoff and explicit timeout budget | Reliable and controlled failure semantics | ✓ |

**User's choice:** Bounded retries with deterministic backoff and explicit timeout budget
**Notes:** Matches LLM-03 requirement for resilient but bounded behavior.

---

## Malformed JSON repair and deterministic fallback

| Option | Description | Selected |
|--------|-------------|----------|
| Fail immediately | Clear behavior but poor resilience | |
| Unlimited repair attempts | Higher recovery chance but unbounded complexity/time | |
| One repair attempt, then deterministic keyword fallback analyzer | Balanced resilience and deterministic completion | ✓ |

**User's choice:** One repair attempt, then deterministic keyword fallback analyzer
**Notes:** Directly satisfies LLM-04 while preserving pipeline continuity.

---

## Execution granularity

| Option | Description | Selected |
|--------|-------------|----------|
| Batch multiple submissions per call | Better throughput, more complex error isolation | |
| Process one incorrect submission per call in stable input order | Simpler traceability and deterministic behavior | ✓ |
| Randomized ordering for throughput | Harder debugging and reproducibility | |

**User's choice:** Process one incorrect submission per call in stable input order
**Notes:** Keeps prototype behavior predictable for downstream phases and tests.

## the agent's Discretion

- Exact timeout/backoff constants.
- Internal module/function naming for extraction pipeline pieces.

## Deferred Ideas

None.
