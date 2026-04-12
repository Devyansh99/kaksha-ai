from src.pipeline.contracts import validate_row_contract
from src.pipeline.cleaning import clean_row


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


def test_valid_row_passes_contract() -> None:
    is_valid, reason = validate_row_contract(_valid_row())

    assert is_valid is True
    assert reason is None


def test_invalid_field_types_are_dropped() -> None:
    row = _valid_row()
    row["question_text"] = 42

    is_valid, reason = validate_row_contract(row)

    assert is_valid is False
    assert reason == "invalid_field_type"


def test_timestamp_normalization_to_utc_iso() -> None:
    row = _valid_row()
    row["timestamp"] = "2026-04-12T15:30:00+05:30"

    cleaned, reason = clean_row(row)

    assert reason is None
    assert cleaned is not None
    assert cleaned["timestamp"] == "2026-04-12T10:00:00Z"


def test_invalid_timestamp_is_dropped() -> None:
    row = _valid_row()
    row["timestamp"] = "not-a-valid-date"

    cleaned, reason = clean_row(row)

    assert cleaned is None
    assert reason == "invalid_timestamp"
