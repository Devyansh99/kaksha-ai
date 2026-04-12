# Phase 1: Data Contracts and Cleaning - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-12
**Phase:** 01-data-contracts-and-cleaning
**Areas discussed:** Schema contract and malformed policy, Timestamp normalization policy, Incorrect-attempt filtering rules, Drop logging output format

---

## Schema contract and malformed policy

| Option | Description | Selected |
|--------|-------------|----------|
| Strict required fields, drop if any missing | Simple and deterministic for prototype; malformed rows logged | ✓ |
| Partial fill with defaults where possible | Keeps more rows but can hide data quality issues | |
| Agent decide | Leave exact rule to planning/research | |

**User's choice:** Strict required fields, drop if any missing
**Notes:** Favor deterministic behavior for prototype reliability.

---

## Timestamp normalization policy

| Option | Description | Selected |
|--------|-------------|----------|
| Parse common ISO/date formats; normalize to UTC ISO-8601 | Reliable for aggregation and ordering | ✓ |
| Keep raw timestamp strings unchanged | Fastest, but weaker consistency guarantees | |
| Agent decide | Leave exact policy to planning/research | |

**User's choice:** Parse common ISO/date formats; normalize to UTC ISO-8601
**Notes:** Prioritizes stable downstream ordering and scoring.

---

## Incorrect-attempt filtering rules

| Option | Description | Selected |
|--------|-------------|----------|
| Treat non-boolean/missing as malformed and drop | Avoids silent logic errors in incorrect-attempt filtering | ✓ |
| Assume missing means incorrect | Retains rows but risks false misconception analysis | |
| Agent decide | Leave exact behavior to planning/research | |

**User's choice:** Treat non-boolean/missing as malformed and drop
**Notes:** Preserves contract integrity before LLM analysis.

---

## Drop logging output format

| Option | Description | Selected |
|--------|-------------|----------|
| Both console summary and structured JSON/JSONL drop log file | Best debuggability with low complexity | ✓ |
| Console summary only | Fastest implementation, less audit detail | |
| Agent decide | Leave exact output to planning/research | |

**User's choice:** Both console summary and structured JSON/JSONL drop log file
**Notes:** Supports both quick visibility and machine-readable diagnostics.

## the agent's Discretion

- Parser/library-level implementation specifics.
- Exact drop-log file naming and storage path.

## Deferred Ideas

None.
