---
phase: 04-quality-signals-and-evaluation
status: complete
source: gsd-plan-phase
created: 2026-04-12
---

# Phase 4 Research: Quality Signals and Evaluation

## Objective

Research how to implement deterministic quality enhancements over Phase 3 outputs: taxonomy normalization, confidence visibility, and prompt strategy comparison summary.

## Inputs Reviewed

- `.planning/phases/04-quality-signals-and-evaluation/04-CONTEXT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/PROJECT.md`
- `src/pipeline/misconception_prompt.py`
- `src/pipeline/misconception_extractor.py`
- `src/pipeline/report_aggregation.py`
- `src/pipeline/report_pipeline.py`
- `tests/test_resilient_misconception_extraction.py`
- `tests/test_teacher_report_aggregation.py`

## Recommended Implementation Approach

1. Add deterministic taxonomy normalization module with canonical labels, groups, alias rules, and explicit `no_taxonomy_match` handling.
2. Integrate normalization outputs into report payload while preserving `raw_label` and adding normalized fields for traceability.
3. Add confidence visibility with consistent numeric rounding and confidence bands (`low`, `medium`, `high`) for teacher readability.
4. Extend prompt builders to support two strict-JSON strategies (zero-shot and few-shot) using shared deterministic schema constraints.
5. Add strategy comparison helper that evaluates both strategies on the same deterministic input slice and writes a short evidence summary artifact.

## Key Technical Decisions from Research

- Keep deterministic pipeline behavior: no additional model calls for normalization in this phase.
- Reuse existing status policy (`ok`, `json_repaired`, `fallback_used` included; `retry_exhausted` excluded from confidence math).
- Keep A/B comparison metrics compact and auditable:
  - parse success rate,
  - normalized-label coverage,
  - rerun consistency,
  - average confidence.

## Risks and Mitigations

- Risk: taxonomy changes introduce nondeterministic mapping behavior.
  - Mitigation: fixed canonical map + explicit alias precedence + deterministic fallback category.
- Risk: strategy comparison noise from inconsistent sampling.
  - Mitigation: deterministic row ordering and fixed subset policy.
- Risk: confidence interpretation ambiguity for teachers.
  - Mitigation: preserve numeric value and add explicit confidence bands.

## Validation Architecture

- Framework: `pytest`
- Quick command: `venv\Scripts\python -m pytest tests/test_quality_signals.py tests/test_prompt_strategy_comparison.py -q`
- Full command: `venv\Scripts\python -m pytest -q`
- Required checks:
  - QLT-01: deterministic normalization and fallback mapping behavior
  - QLT-02: deterministic A/B comparison summary generation
  - QLT-03: confidence score and confidence band visibility in outputs

## Output

Research complete; ready for validation strategy generation, planning, and checker verification loop.
