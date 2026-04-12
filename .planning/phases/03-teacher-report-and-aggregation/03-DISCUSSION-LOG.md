# Phase 3: Teacher Report and Aggregation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves alternatives considered.

**Date:** 2026-04-12
**Phase:** 03-teacher-report-and-aggregation
**Areas discussed:** Mastery scoring policy, Deterministic report schema, Cohort summary ranking, Evidence snippet policy, Failure-status handling

---

## Mastery scoring policy

| Option | Description | Selected |
|--------|-------------|----------|
| Simple raw accuracy | Easiest but ignores misconception confidence detail from Phase 2 | |
| Time-weighted recency | Useful for temporal drift but adds complexity without explicit phase requirement | |
| Misconception-severity deduction (confidence-weighted) with deterministic clamp | Uses available extraction confidence and aligns with actionable teaching signal | ✓ |

**User's choice:** Misconception-severity deduction (confidence-weighted) with deterministic clamp
**Notes:** Applied in low-request mode using recommended default for phase-fit and determinism.

---

## Deterministic report schema

| Option | Description | Selected |
|--------|-------------|----------|
| List-based flexible schema | Easy to append but weaker deterministic indexing by student/concept | |
| Student-keyed concept map with deterministic sorted ordering and stable numeric formatting | Matches PRD/requirements and repeatable output checks | ✓ |
| Mixed schema by source status | Adds complexity and weakens stable consumer contract | |

**User's choice:** Student-keyed concept map with deterministic sorted ordering and stable numeric formatting
**Notes:** Keeps downstream planner/reporter contract stable for Phase 4.

---

## Cohort summary ranking

| Option | Description | Selected |
|--------|-------------|----------|
| Rank by confidence only | Can over-prioritize sparse outliers | |
| Rank by occurrence count, tie-break with avg confidence then label sort | Most teacher-actionable and deterministic tie-breaking | ✓ |
| Manual label priority list | Requires external taxonomy policy not in current phase scope | |

**User's choice:** Rank by occurrence count, tie-break with avg confidence then label sort
**Notes:** Supports deterministic top-misconception ordering.

---

## Evidence snippet policy

| Option | Description | Selected |
|--------|-------------|----------|
| Include all raw attempts | Too verbose for teacher report readability | |
| Up to 3 concise snippets per misconception with question_text and student_answer | Balanced evidence and readability | ✓ |
| No evidence snippets | Fails requirement for concise evidence review | |

**User's choice:** Up to 3 concise snippets per misconception with question_text and student_answer
**Notes:** Directly satisfies RPT-04.

---

## Failure-status handling

| Option | Description | Selected |
|--------|-------------|----------|
| Exclude silently | Hides operational reliability issues from report metadata | |
| Exclude from misconception evidence but track in report metadata counters | Preserves deterministic quality accounting without noisy evidence pollution | ✓ |
| Treat as fallback misconception entries | Risks inventing unsupported misconception evidence | |

**User's choice:** Exclude from misconception evidence but track in report metadata counters
**Notes:** Preserves report quality while keeping reliability visibility.

## the agent's Discretion

- Exact function/module names for report aggregation internals.
- Exact evidence text trimming thresholds.

## Deferred Ideas

None.
