from src.pipeline.misconception_prompt import (
    REQUIRED_MISCONCEPTION_KEYS,
    REQUIRED_RESPONSE_KEYS,
    build_misconception_prompt,
)


def test_prompt_requires_json_only_contract() -> None:
    row = {
        "student_id": "S-100",
        "concept": "Fractions",
        "question_text": "1/3 + 1/6 = ?",
        "student_answer": "2/9",
    }

    prompt = build_misconception_prompt(row)

    assert "Return only valid JSON" in prompt
    assert all(key in prompt for key in REQUIRED_RESPONSE_KEYS)
    assert all(key in prompt for key in REQUIRED_MISCONCEPTION_KEYS)
