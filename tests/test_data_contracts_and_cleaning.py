from src.pipeline.contracts import validate_row_contract


def _valid_row() -> dict:
    return {
        "student_id": "S-001",
        "subject": "Math",
        "concept": "Fractions",
        "question_text": "1/2 + 1/4 = ?",
        "correct_answer": "3/4",
        "student_answer": "2/6",
        "is_correct": False,
        "timestamp": "2026-04-12T10:00:00Z",
    }


def test_missing_required_fields_are_dropped() -> None:
    row = _valid_row()
    del row["student_id"]

    is_valid, reason = validate_row_contract(row)

    assert is_valid is False
    assert reason == "missing_required_field"


def test_invalid_field_types_are_dropped() -> None:
    row = _valid_row()
    row["question_text"] = 42

    is_valid, reason = validate_row_contract(row)

    assert is_valid is False
    assert reason == "invalid_field_type"
