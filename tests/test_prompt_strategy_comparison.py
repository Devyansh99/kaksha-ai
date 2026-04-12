from src.pipeline.misconception_prompt import (
    REQUIRED_MISCONCEPTION_KEYS,
    REQUIRED_RESPONSE_KEYS,
    build_misconception_prompt_few_shot,
    build_misconception_prompt_zero_shot,
)
from src.pipeline.strategy_comparison import (
    compare_prompt_strategies,
    write_strategy_summary,
)


def test_prompt_strategy_builders_are_distinct_and_json_strict() -> None:
    row = {
        "student_id": "S-100",
        "concept": "Fractions",
        "question_text": "1/3 + 1/6 = ?",
        "student_answer": "2/9",
    }

    zero_shot_prompt = build_misconception_prompt_zero_shot(row)
    few_shot_prompt = build_misconception_prompt_few_shot(row)

    assert zero_shot_prompt != few_shot_prompt

    for prompt in (zero_shot_prompt, few_shot_prompt):
        assert "Return only valid JSON" in prompt
        assert "Do not include markdown fences" in prompt
        assert all(key in prompt for key in REQUIRED_RESPONSE_KEYS)
        assert all(key in prompt for key in REQUIRED_MISCONCEPTION_KEYS)


def test_strategy_comparison_summary_contains_required_metrics(tmp_path) -> None:
    rows = [
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "1/2 + 1/3 = ?",
            "student_answer": "2/5",
        },
        {
            "student_id": "S-2",
            "concept": "Fractions",
            "question_text": "1/3 + 1/6 = ?",
            "student_answer": "2/9",
        },
    ]

    def analyzer(prompt: str, row: dict) -> dict:
        if "Few-shot examples" in prompt:
            return {
                "status": "ok",
                "misconceptions": [
                    {
                        "label": "denominator error",
                        "rationale": "added denominators",
                        "confidence": 0.88,
                    }
                ],
            }
        return {
            "status": "json_repaired" if row["student_id"] == "S-1" else "fallback_used",
            "misconceptions": [
                {
                    "label": "structure confusion",
                    "rationale": "concept mismatch",
                    "confidence": 0.61,
                }
            ],
        }

    result = compare_prompt_strategies(rows, analyzer)

    for strategy in ("zero_shot", "few_shot"):
        assert "parse_success_rate" in result["metrics"][strategy]
        assert "normalized_label_coverage" in result["metrics"][strategy]
        assert "rerun_consistency" in result["metrics"][strategy]
        assert "avg_confidence" in result["metrics"][strategy]

    summary_path = tmp_path / "04-AB-RESULTS.md"
    write_strategy_summary(result, str(summary_path))

    summary_text = summary_path.read_text(encoding="utf-8")
    assert "parse_success_rate" in summary_text
    assert "normalized_label_coverage" in summary_text
    assert "rerun_consistency" in summary_text
    assert "avg_confidence" in summary_text
