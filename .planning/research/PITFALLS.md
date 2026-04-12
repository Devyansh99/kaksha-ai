# Domain Pitfalls: Misconception Analyzer Pipeline

**Domain:** LLM + data pipeline + educational misconception classification
**Researched:** 2026-04-12

## Suggested Phase Mapping

- **Phase 1 - Data Ingestion and Cleaning:** schema validation, malformed-row handling, timestamp normalization, drop logging
- **Phase 2 - Misconception Extraction (LLM):** prompt contract, response parsing, retries/fallbacks, provider limits
- **Phase 3 - Aggregation and Reporting:** mastery scoring, grouping logic, report schema validation
- **Phase 4 - Evaluation and Guardrails:** quality checks, drift checks, edge-case tests, privacy/safety verification

## Critical Pitfalls

### 1) Label Leakage via Prompt Context
**What goes wrong:** The prompt leaks `correct_answer` or obvious evaluative cues in a way that makes the model infer the target label instead of diagnosing the student's reasoning error.
**Why this is domain-specific:** Misconception classification should explain wrong thinking patterns, not just compare string mismatch against the right answer.
**Warning signs:**
- Misconception outputs mirror answer-key wording rather than student reasoning.
- Very high confidence classifications even for ambiguous student responses.
- Nearly identical misconception labels across different wrong-answer patterns.
**Prevention strategy:**
- Separate fields used for diagnosis from fields used for scoring.
- Ask the model to cite evidence tokens from `student_answer` and `question_text`.
- Add adversarial test rows where wrong answers share surface form but imply different misconceptions.
**Phase to address:** **Phase 2** (prompt design) and verify in **Phase 4**.

### 2) Free-Form LLM Output Breaking the Pipeline Contract
**What goes wrong:** LLM returns prose, markdown, or partial JSON, causing parser errors or silent fallback overuse.
**Why this is domain-specific:** The whole pipeline depends on strict machine-readable misconception objects per incorrect attempt.
**Warning signs:**
- JSON decode failures >10% of incorrect rows.
- Frequent keys missing from returned misconception objects.
- Spike in fallback classifier usage without clear API outage.
**Prevention strategy:**
- Use explicit JSON schema instructions and a deterministic output envelope.
- Validate each response against a strict schema before aggregation.
- Implement bounded retry with a "repair" prompt, then deterministic fallback.
**Phase to address:** **Phase 2**.

### 3) Conflating "Wrong Answer" with "Misconception"
**What goes wrong:** Every incorrect response is treated as a conceptual misconception, even when error is due to typo, language ambiguity, or careless slip.
**Why this is domain-specific:** Education analytics needs pedagogically meaningful error categories, not generic wrong/correct tagging.
**Warning signs:**
- Misconception count is nearly equal to count of incorrect responses.
- Labels such as "does not understand concept" appear too often.
- Teacher review says labels are too coarse to act on.
**Prevention strategy:**
- Include an explicit "insufficient evidence / non-conceptual error" class.
- Require model rationale grounded in concept-specific cues.
- Add post-processing thresholds so low-evidence cases do not become hard misconception labels.
**Phase to address:** **Phase 2**, with audit checks in **Phase 4**.

### 4) Timestamp Misinterpretation Distorting Mastery Trends
**What goes wrong:** Mixed formats/time zones or parse failures produce incorrect event order, skewing recency-weighted mastery.
**Why this is domain-specific:** Student misconception trajectory is time-sensitive; bad ordering creates false learning/regression signals.
**Warning signs:**
- Negative or implausible time gaps between attempts.
- Mastery jumps that contradict answer sequence.
- Large fraction of timestamps defaulting to null/current time.
**Prevention strategy:**
- Enforce strict timestamp parser with explicit accepted formats.
- Normalize to one timezone and log parse failures with row IDs.
- Use stable sorting keys and deterministic tie-breaking.
**Phase to address:** **Phase 1** (parsing) and **Phase 3** (scoring logic).

### 5) Concept Taxonomy Drift (Same Concept, Multiple Names)
**What goes wrong:** Equivalent concepts (for example, "fractions" vs "fraction arithmetic") are treated as different buckets, fragmenting mastery and misconception counts.
**Why this is domain-specific:** Educational reports require consistent concept-level aggregation to be actionable for teachers.
**Warning signs:**
- Many low-frequency concept buckets with near-duplicate names.
- Same student shows conflicting mastery across semantically identical concepts.
- Teacher report appears noisy with overly granular categories.
**Prevention strategy:**
- Define a canonical concept dictionary and normalization rules.
- Map aliases during cleaning before LLM analysis.
- Add a validation check for new unseen concepts.
**Phase to address:** **Phase 1** and **Phase 3**.

### 6) Fallback Classifier Becoming the Primary Path
**What goes wrong:** Keyword mock fallback silently handles most rows due to rate limits/timeouts, reducing quality while appearing "successful."
**Why this is domain-specific:** Prototype reliability requirement can accidentally hide LLM quality regressions in misconception detection.
**Warning signs:**
- Fallback usage rate is high (>20%) during normal runs.
- Same generic misconceptions repeated across subjects/concepts.
- Run succeeds but qualitative output quality degrades.
**Prevention strategy:**
- Log route metadata per row (`llm_primary` vs `fallback`).
- Set alert threshold for fallback ratio and fail quality gate if exceeded.
- Compare a sample of fallback vs LLM labels each run.
**Phase to address:** **Phase 2**, monitored in **Phase 4**.

### 7) Aggregation Double-Counting Attempts
**What goes wrong:** Duplicate rows, retry artifacts, or incorrect grouping logic inflate misconception frequency and distort mastery.
**Why this is domain-specific:** Teacher interventions rely on accurate per-student per-concept frequency and trend counts.
**Warning signs:**
- Attempt counts exceed raw input row counts after cleaning.
- Duplicate misconception entries with identical timestamps.
- Mastery scores inconsistent across repeated runs on same data.
**Prevention strategy:**
- Define an idempotent attempt key (student_id + concept + question_text + timestamp).
- De-duplicate before scoring and during aggregation.
- Add deterministic regression test with fixed fixture data.
**Phase to address:** **Phase 1** and **Phase 3**.

### 8) Pedagogically Unsafe or Non-Actionable Labels
**What goes wrong:** Labels are judgmental (for example, "weak student") or too abstract to guide instruction.
**Why this is domain-specific:** Educational outputs should support teaching actions, not stigmatize learners.
**Warning signs:**
- Labels describe student ability, not misconception pattern.
- Teachers cannot map labels to remediation steps.
- Similar reasoning errors receive inconsistent label wording.
**Prevention strategy:**
- Constrain label ontology to neutral, concept-linked misconception types.
- Add style/wording guardrails in prompt and post-validation.
- Store actionable recommendation snippets per misconception category.
**Phase to address:** **Phase 2** (label generation) and **Phase 4** (quality review).

## Phase-Specific Warning Matrix

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| Data cleaning and schema enforcement | Timestamp/order corruption, taxonomy drift, duplicate attempts | Strict parsers, canonical concept map, idempotent dedup keys |
| LLM misconception extraction | JSON contract breaks, label leakage, overuse of fallback, non-actionable labels | Schema validation, evidence-grounded prompts, fallback thresholding, ontology constraints |
| Aggregation and scoring | Double counting, unstable mastery signals | Deterministic grouping, stable sorting, reproducible scoring tests |
| Evaluation and guardrails | Hidden quality regressions despite successful run | Track fallback ratio, teacher-facing sample review, fixed benchmark set |

## Practical Minimum for This 4-Hour Prototype

- Track per-row processing status (`cleaned`, `llm_ok`, `llm_retry_ok`, `fallback_used`, `dropped`).
- Enforce strict JSON schema before report aggregation.
- Add one small benchmark fixture set with expected misconception categories.
- Fail fast on report schema violations, but do not crash on single-row errors.
