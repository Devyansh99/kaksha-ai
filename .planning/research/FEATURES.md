# Feature Landscape

**Project:** Misconception Analyzer Pipeline
**Domain:** Educational misconception-analysis pipeline (teacher-facing analytics output)
**Researched:** 2026-04-12
**Scope Lens:** Internship v1 prototype (~4 hours), local execution, JSON deliverable (no UI)
**Confidence:** MEDIUM (grounded in project PRD + common learning-analytics patterns)

## Table Stakes (Must-Have for v1)

Features users expect for this kind of pipeline. Missing these makes the prototype feel broken.

| Feature | Why Expected | Complexity | v1 Inclusion | Dependencies |
|---------|--------------|------------|--------------|--------------|
| Input schema validation and row-level cleaning | Teacher trust depends on reliable ingestion of messy classroom data | Low | Yes (required) | Student log schema definition; parser for timestamp/required fields |
| Malformed-row drop logging (with reason) | Ops/debug visibility is mandatory when datasets include bad rows | Low | Yes (required) | Validation stage; structured logger |
| Incorrect-attempt filtering before misconception analysis | Misconception inference should run only on wrong answers to reduce noise/cost | Low | Yes (required) | Correctness flag normalization |
| Strict structured LLM output contract (JSON-only) | Downstream aggregation/reporting needs predictable machine-readable output | Medium | Yes (required) | Prompt template; JSON schema; response parser |
| Resilience on LLM failures (timeout/error/bad JSON) | Classroom workflows cannot fail hard when model calls fail | Medium | Yes (required) | Retry/fallback policy; exception handling; mock keyword fallback |
| Per-student, per-concept mastery score | Core teacher need is understanding who struggles with what concept | Medium | Yes (required) | Cleaned records; aggregation logic; scoring formula |
| Teacher-facing aggregate JSON report (`teacher_report.json`) | Explicit project output contract and minimum useful artifact for educators | Medium | Yes (required) | Aggregation module; serialization contract |
| Reproducible local run path (README + env config) | Expected even for prototypes so others can run and validate quickly | Low | Yes (required) | Env var config; simple entrypoint |

## Differentiators (High-Value, Keep Lightweight in v1)

Features that make this prototype stand out without exploding scope.

| Feature | Value Proposition | Complexity | v1 Strategy | Dependencies |
|---------|-------------------|------------|-------------|--------------|
| Misconception taxonomy normalization (e.g., map free-text causes to canonical labels) | Produces cleaner analytics and cross-student comparability for teachers | Medium | Include a small fixed taxonomy (5-10 labels) | Prompt rubric; post-processing mapper |
| Confidence score per identified misconception | Helps teachers prioritize intervention rather than treating all flags equally | Medium | Include heuristic confidence (LLM self-score + parse quality checks) | Structured output fields; validator |
| Evidence snippets in report (`question_text`, `student_answer`) | Increases explainability and teacher trust in each misconception tag | Low | Include compact evidence fields per finding | Source record linkage |
| Prompt strategy A/B comparison summary (bonus) | Shows engineering rigor and can justify prompt choice for future scaling | Medium | Run tiny A/B on same subset and store short comparison note | Two prompt templates; evaluation rubric |
| Concept-level cohort summary (top misconceptions per concept) | Gives immediate class-level actionability beyond student-by-student view | Low | Add derived summary section in same JSON | Aggregated misconception counts |

## Anti-Features (Do Not Build in v1)

Features that look attractive but are poor fit for this prototype's time and constraints.

| Anti-Feature | Why Avoid for v1 | What to Do Instead |
|--------------|------------------|--------------------|
| Full teacher dashboard UI | Out of scope; increases frontend and product complexity with little impact on core validation | Keep output JSON-first; optionally provide a tiny CLI pretty-print |
| Real-time streaming ingestion | Adds infra/event complexity not needed for demo datasets | Use batch file ingestion (`student_logs.json`) |
| Heavy custom ML training pipeline | Requires labeled data, experimentation cycle, and MLOps overhead | Use LLM + rule-based fallback for initial validation |
| Multi-tenant auth/roles and production security hardening | Valuable later but not needed for prototype acceptance criteria | Keep local script + env-var API key handling |
| Advanced causal learning analytics claims | Risk of overpromising educational impact without rigorous evaluation design | Frame results as signals, not definitive diagnosis |
| Multi-language deep localization | High surface area for prompts, taxonomy, and QA | Keep single-language v1 and design extensible taxonomy keys |

## Feature Dependencies (Build Order)

```text
Schema contract + sample data
  -> Data cleaning + malformed row logging
    -> Incorrect-attempt filtering
      -> Prompt builder + strict JSON schema
        -> LLM call resilience + fallback path
          -> Misconception normalization + confidence scoring
            -> Student/concept aggregation + mastery score
              -> teacher_report.json (student view + cohort summary)
                -> Optional prompt-strategy A/B note
```

## v1 MVP Recommendation

Prioritize these in order:

1. Data cleaning + malformed row logging
2. Strict JSON-output misconception extraction with failure resilience
3. Per-student/per-concept mastery aggregation and teacher report output
4. One lightweight differentiator: misconception taxonomy normalization

Defer to post-v1:

- Dashboard/UI layer
- Real-time ingestion
- Custom model training and advanced analytics claims
- Enterprise-grade auth/security scope

## Practical Scope Check (4-hour constraint)

- Keep modules separable and linear (ingest -> analyze -> aggregate).
- Prefer deterministic JSON schemas and minimal branching.
- Implement exactly one scoring method (simple accuracy or lightweight weighted variant), then document tradeoff.
- Add only one standout differentiator (taxonomy normalization) to avoid scope creep.
