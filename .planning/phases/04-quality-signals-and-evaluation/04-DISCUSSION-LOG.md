# Phase 4: Quality Signals and Evaluation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-04-12
**Phase:** 04-quality-signals-and-evaluation
**Areas discussed:** Taxonomy design scope, Normalization method policy, Prompt strategy comparison, Confidence visibility

---

## Taxonomy design scope

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed versioned taxonomy | Stable canonical labels/groups for deterministic reporting and diff stability | ✓ |
| Flexible free-form labels | Keep model labels unchanged with no canonical map | |
| Hybrid ad-hoc edits | Manually adjust labels per run when needed | |

**User's choice:** Fixed versioned taxonomy (best-practice default requested)
**Notes:** User asked to apply best options for all areas.

---

## Normalization method policy

| Option | Description | Selected |
|--------|-------------|----------|
| Deterministic rule-first mapping | Exact/normalized/alias rules, no extra model call | ✓ |
| LLM-assisted normalization | Add a second model pass to rewrite labels | |
| Manual-only normalization | Human review step for each output before mapping | |

**User's choice:** Deterministic rule-first mapping (best-practice default requested)
**Notes:** Keeps existing deterministic pipeline behavior consistent with Phase 2/3 constraints.

---

## Prompt strategy comparison

| Option | Description | Selected |
|--------|-------------|----------|
| Zero-shot vs few-shot strict JSON | Compare two practical prompt styles on same input slice and report concise metrics | ✓ |
| Zero-shot vs chain-of-thought | Compare with reasoning-heavy style (higher variability risk) | |
| Single-strategy only | Skip A/B and choose one strategy without evidence summary | |

**User's choice:** Zero-shot vs few-shot strict JSON (best-practice default requested)
**Notes:** Matches Phase 4 requirement for recorded strategy comparison while keeping scope small.

---

## Confidence visibility

| Option | Description | Selected |
|--------|-------------|----------|
| Numeric + confidence bands | Keep 0-1 numeric confidence and add low/medium/high interpretation bands | ✓ |
| Numeric only | Show raw numbers without qualitative bands | |
| Band only | Hide numeric values and display categories only | |

**User's choice:** Numeric + confidence bands (best-practice default requested)
**Notes:** Preserves technical fidelity while improving teacher readability.

---

## the agent's Discretion

- Exact taxonomy alias dictionary values.
- Deterministic sampling size for A/B comparison when input size is large.

## Deferred Ideas

None.
