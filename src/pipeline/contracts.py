from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = [
    "student_id",
    "subject",
    "concept",
    "question_text",
    "correct_answer",
    "student_answer",
    "is_correct",
    "timestamp",
]

TEXT_FIELDS = {
    "student_id",
    "subject",
    "concept",
    "question_text",
    "correct_answer",
    "student_answer",
    "timestamp",
}


def validate_row_contract(row: dict) -> tuple[bool, str | None]:
    for field in REQUIRED_FIELDS:
        if field not in row or row[field] is None:
            return False, "missing_required_field"

        value = row[field]
        if isinstance(value, str) and value.strip() == "":
            return False, "missing_required_field"

        if field in TEXT_FIELDS and not isinstance(value, str):
            return False, "invalid_field_type"

    return True, None
