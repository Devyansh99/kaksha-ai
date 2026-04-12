from __future__ import annotations

import json

REQUIRED_RESPONSE_KEYS = [
    "student_id",
    "concept",
    "question_text",
    "student_answer",
    "misconceptions",
]

REQUIRED_MISCONCEPTION_KEYS = [
    "label",
    "rationale",
    "confidence",
]


def _build_prompt(row: dict, few_shot_examples: list[dict] | None = None) -> str:
    schema_example = {
        "student_id": row.get("student_id", ""),
        "concept": row.get("concept", ""),
        "question_text": row.get("question_text", ""),
        "student_answer": row.get("student_answer", ""),
        "misconceptions": [
            {
                "label": "",
                "rationale": "",
                "confidence": 0.0,
            }
        ],
    }

    examples_block = ""
    if few_shot_examples:
        examples_block = (
            "Few-shot examples (strict JSON shape):\n"
            f"{json.dumps(few_shot_examples, ensure_ascii=True)}\n\n"
        )

    return (
        "You are an educational misconception analyzer. "
        "Return only valid JSON. "
        "Do not include markdown fences, comments, or explanatory text.\n\n"
        "Required top-level keys: student_id, concept, question_text, student_answer, misconceptions.\n"
        "Each misconception item must contain: label, rationale, confidence.\n"
        "Confidence must be a number between 0 and 1.\n\n"
        f"{examples_block}"
        "Analyze this incorrect submission and output exactly one JSON object:\n"
        f"{json.dumps(schema_example, ensure_ascii=True)}"
    )


def build_misconception_prompt_zero_shot(row: dict) -> str:
    return _build_prompt(row)


def build_misconception_prompt_few_shot(row: dict) -> str:
    few_shot_examples = [
        {
            "student_id": "S-EX-1",
            "concept": "Fractions",
            "question_text": "1/2 + 1/3 = ?",
            "student_answer": "2/5",
            "misconceptions": [
                {
                    "label": "Denominator addition",
                    "rationale": "Student added denominators directly.",
                    "confidence": 0.88,
                }
            ],
        }
    ]
    return _build_prompt(row, few_shot_examples=few_shot_examples)


def build_misconception_prompt(row: dict) -> str:
    return build_misconception_prompt_zero_shot(row)
