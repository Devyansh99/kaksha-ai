from src.pipeline.contracts import validate_row_contract
from src.pipeline.cleaning import clean_row
from src.pipeline.filtering import filter_incorrect_rows
from src.pipeline.ingest import run_ingestion_pipeline

import json


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


def test_only_incorrect_rows_forwarded() -> None:
    row_false = _valid_row()
    row_true = _valid_row()
    row_true["is_correct"] = True

    forwarded, dropped = filter_incorrect_rows([row_false, row_true])

    assert len(forwarded) == 1
    assert forwarded[0]["is_correct"] is False
    assert dropped == []


def test_invalid_is_correct_rows_are_dropped() -> None:
    invalid_row = _valid_row()
    invalid_row["is_correct"] = "false"

    forwarded, dropped = filter_incorrect_rows([invalid_row])

    assert forwarded == []
    assert len(dropped) == 1
    assert dropped[0]["reason_code"] == "invalid_is_correct"


def test_drop_log_written_with_reason_codes(tmp_path) -> None:
    rows = [
        {
            "student_id": "S-001",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "correct_answer": "3/4",
            "student_answer": "2/6",
            "is_correct": False,
            "timestamp": "2026-04-12T10:00:00Z",
        },
        {
            "student_id": "S-002",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/2 + 1/3 = ?",
            "correct_answer": "5/6",
            "student_answer": "2/5",
            "is_correct": "false",
            "timestamp": "2026-04-12T10:00:00Z",
        },
        {
            "student_id": "S-003",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/3 + 1/3 = ?",
            "correct_answer": "2/3",
            "student_answer": "2/3",
            "is_correct": True,
            "timestamp": "2026-04-12T10:00:00Z",
        },
    ]

    input_file = tmp_path / "student_logs.json"
    input_file.write_text(json.dumps(rows), encoding="utf-8")
    drop_log = tmp_path / "drop_log.jsonl"

    forwarded, _summary = run_ingestion_pipeline(
        str(input_file), drop_log_path=str(drop_log)
    )

    assert drop_log.exists()
    records = [
        json.loads(line)
        for line in drop_log.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(forwarded) == 1
    assert forwarded[0]["is_correct"] is False
    assert any(record["reason_code"] == "invalid_is_correct" for record in records)


def test_console_summary_has_reason_counts(tmp_path, capsys) -> None:
    rows = [
        {
            "student_id": "S-001",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "correct_answer": "3/4",
            "student_answer": "2/6",
            "is_correct": False,
            "timestamp": "2026-04-12T10:00:00Z",
        },
        {
            "student_id": "S-004",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/2 + 1/5 = ?",
            "correct_answer": "7/10",
            "student_answer": "6/10",
            "is_correct": False,
            "timestamp": "not-a-valid-date",
        },
    ]

    input_file = tmp_path / "student_logs.json"
    input_file.write_text(json.dumps(rows), encoding="utf-8")
    run_ingestion_pipeline(str(input_file), drop_log_path=str(tmp_path / "drop_log.jsonl"))

    output = capsys.readouterr().out
    assert "total_rows" in output
    assert "valid_rows" in output
    assert "dropped_rows" in output
    assert "reason_counts" in output
