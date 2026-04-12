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


def build_misconception_prompt(row: dict) -> str:
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

    return (
        "You are an educational misconception analyzer. "
        "Return only valid JSON. "
        "Do not include markdown fences, comments, or explanatory text.\n\n"
        "Required top-level keys: student_id, concept, question_text, student_answer, misconceptions.\n"
        "Each misconception item must contain: label, rationale, confidence.\n"
        "Confidence must be a number between 0 and 1.\n\n"
        "Analyze this incorrect submission and output exactly one JSON object:\n"
        f"{json.dumps(schema_example, ensure_ascii=True)}"
    )
