# Architecture: Misconception Analyzer Pipeline

**Project:** Misconception Analyzer Pipeline  
**Date:** 2026-04-12  
**Scope:** Lightweight local prototype (not production)

## 1) Recommended System Structure (Prototype)

Use a single-process, file-in/file-out pipeline with clear module boundaries:

1. `ingest` - Load raw JSON rows
2. `validate_clean` - Schema checks, type normalization, malformed row dropping + logging
3. `select_candidates` - Keep only incorrect responses for misconception analysis
4. `analyze_misconceptions` - LLM-first analyzer (strict JSON), fallback to keyword rules
5. `aggregate_score` - Per-student + per-concept aggregation and mastery scoring
6. `write_report` - Emit `teacher_report.json` and run summary metadata

Keep orchestration in one runner (`main.py`) and keep each step as a pure function where possible.

## 2) Component Boundaries

| Component | Responsibility | Input Contract | Output Contract | Notes |
|---|---|---|---|---|
| `InputReader` | Read `student_logs.json` | File path | `list[dict]` raw rows | No business logic here |
| `RowValidatorCleaner` | Validate required fields and normalize values | Raw rows | `clean_rows`, `dropped_rows_log` | Never throws on bad rows; drops + logs |
| `CandidateFilter` | Identify rows eligible for misconception detection | `clean_rows` | `analysis_rows` (mostly `is_correct == false`) | Keep deterministic |
| `PromptBuilder` | Build strict JSON-only prompt for each row/batch | `analysis_rows` | prompt text payload(s) | Include explicit schema in prompt |
| `LLMClient` | Call OpenRouter (Qwen 3.6 free) with timeout/retry | prompt payload | raw model text response | Provider/network concerns isolated |
| `LLMResponseParser` | Parse and validate JSON response | raw model response | normalized misconception objects | On parse failure, signal fallback path |
| `FallbackAnalyzer` | Rule-based misconception tags when LLM fails | `analysis_rows` | misconception objects | Guarantees end-to-end run |
| `AggregatorScorer` | Build teacher view grouped by student + concept and compute mastery | `clean_rows` + misconceptions | report domain object | Single source of scoring logic |
| `ReportWriter` | Write final output file | report object | `teacher_report.json` | Stable output schema |
| `PipelineRunner` | Orchestrate step order, collect run stats | config + paths | final artifacts + logs | Coordinates, does not analyze |

## 3) Data Flow Direction

Data should flow one way (left to right), with no step mutating prior stage outputs in place.

```text
student_logs.json
  -> InputReader
  -> RowValidatorCleaner
      -> dropped_rows_log.jsonl (side artifact)
  -> CandidateFilter
  -> (PromptBuilder -> LLMClient -> LLMResponseParser)
       if failure/timeout/malformed JSON
       -> FallbackAnalyzer
  -> AggregatorScorer
  -> ReportWriter
  -> teacher_report.json
```

### Data shape progression

1. **Raw row**: potentially malformed source record
2. **Clean row**: validated/normalized record with required fields present
3. **Analysis item**: clean incorrect-answer row prepared for misconception extraction
4. **Misconception result**: structured tags/reasons/confidence
5. **Teacher aggregate**: grouped by `student_id` and `concept` with mastery score

## 4) Lightweight Directory Layout

```text
.
├─ student_logs.json
├─ teacher_report.json                  # output
├─ logs/
│  └─ dropped_rows_log.jsonl            # malformed row audit
├─ src/
│  ├─ main.py                           # PipelineRunner
│  ├─ types.py                          # typed dicts/dataclasses (optional but helpful)
│  ├─ ingest.py
│  ├─ validate_clean.py
│  ├─ select_candidates.py
│  ├─ llm/
│  │  ├─ prompt_builder.py
│  │  ├─ client.py
│  │  └─ parser.py
│  ├─ fallback.py
│  ├─ aggregate_score.py
│  └─ write_report.py
└─ tests/
   ├─ test_validate_clean.py
   ├─ test_aggregate_score.py
   └─ test_pipeline_smoke.py
```

This keeps concerns separated while staying small enough for internship prototype speed.

## 5) Suggested Build Order (Fastest Path to Working Demo)

1. **Define contracts + output schema first**
   - Freeze expected `teacher_report.json` structure and internal data shapes.
   - Reason: avoids rewrites when adding LLM and fallback.

2. **Implement ingestion + cleaning + drop logging**
   - Build `InputReader` and `RowValidatorCleaner` with malformed row tolerance.
   - Add unit tests for malformed rows and type normalization.

3. **Implement aggregation + mastery scoring with mock misconceptions**
   - Build `AggregatorScorer` and `ReportWriter` using temporary/mock misconception inputs.
   - Reason: establishes end-state report early.

4. **Add LLM path (prompt -> call -> parse) with strict JSON enforcement**
   - Add timeout/retry and parser validation.
   - If parse fails, return explicit failure signal.

5. **Add fallback analyzer and failure routing**
   - Route LLM failures/timeouts/malformed JSON to keyword-based analyzer.
   - Ensure pipeline never crashes and always outputs report.

6. **Integrate end-to-end runner + smoke test**
   - One command execution from input file to output file.
   - Verify report produced even under simulated LLM failure.

7. **(Optional bonus) compare two prompt strategies**
   - Keep behind simple config flag.

## 6) Prototype Guardrails

- Keep everything synchronous and local for simplicity.
- Prefer plain functions over classes unless boundary isolation needs state.
- Log enough to debug (`rows_in`, `rows_clean`, `rows_dropped`, `llm_failures`, `fallback_used`).
- Fail closed on LLM parse issues (fallback), not open with ambiguous text.
- Do not optimize for scale now; optimize for correctness and resilience.

## 7) Minimal Success Criteria

- Pipeline accepts `student_logs.json` with malformed rows and does not crash.
- `teacher_report.json` is always produced.
- Report is keyed by student and concept and includes mastery score + misconceptions.
- LLM failure scenarios still produce valid output through fallback.
