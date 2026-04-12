from src.pipeline.misconception_prompt import (
    REQUIRED_MISCONCEPTION_KEYS,
    REQUIRED_RESPONSE_KEYS,
    build_misconception_prompt_few_shot,
    build_misconception_prompt_zero_shot,
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
