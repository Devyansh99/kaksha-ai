from src.pipeline.report_aggregation import (
    aggregate_by_student_concept,
    build_cohort_summary,
    compute_mastery_score,
)
from src.pipeline.report_pipeline import build_teacher_report
from src.pipeline.report_writer import write_teacher_report


def test_mastery_score_is_bounded_and_deterministic() -> None:
    records = [
        {
            "misconceptions": [
                {"label": "A", "rationale": "r", "confidence": 0.9},
                {"label": "B", "rationale": "r", "confidence": 0.8},
            ]
        },
        {
            "misconceptions": [
                {"label": "C", "rationale": "r", "confidence": 0.7},
            ]
        },
    ]

    first = compute_mastery_score(records)
    second = compute_mastery_score(records)

    assert isinstance(first, int)
    assert 0 <= first <= 100
    assert first == second

    rows = [
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "student_answer": "2/6",
            "misconceptions": [{"label": "Denominator addition", "rationale": "r", "confidence": 0.8}],
            "status": "ok",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "1/3 + 1/6 = ?",
            "student_answer": "2/9",
            "misconceptions": [{"label": "Structure", "rationale": "r", "confidence": 0.4}],
            "status": "fallback_used",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "2/3 + 1/3 = ?",
            "student_answer": "3/6",
            "misconceptions": [{"label": "Reduction", "rationale": "r", "confidence": 0.5}],
            "status": "json_repaired",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "1/3 + 1/3 = ?",
            "student_answer": "2/6",
            "misconceptions": [],
            "status": "retry_exhausted",
        },
    ]

    aggregated = aggregate_by_student_concept(rows)

    assert aggregated["metadata"]["rows_excluded_retry_exhausted"] == 1
    score = aggregated["students"]["S-1"]["Fractions"]["mastery_score"]
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_cohort_summary_ranking_is_deterministic() -> None:
    rows = [
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "misconceptions": [{"label": "A", "rationale": "r", "confidence": 0.4}],
            "status": "ok",
        },
        {
            "student_id": "S-2",
            "concept": "Fractions",
            "misconceptions": [{"label": "B", "rationale": "r", "confidence": 0.9}],
            "status": "json_repaired",
        },
        {
            "student_id": "S-3",
            "concept": "Fractions",
            "misconceptions": [{"label": "A", "rationale": "r", "confidence": 0.8}],
            "status": "fallback_used",
        },
        {
            "student_id": "S-4",
            "concept": "Fractions",
            "misconceptions": [{"label": "B", "rationale": "r", "confidence": 0.5}],
            "status": "ok",
        },
        {
            "student_id": "S-5",
            "concept": "Fractions",
            "misconceptions": [{"label": "C", "rationale": "r", "confidence": 1.0}],
            "status": "retry_exhausted",
        },
        {
            "student_id": "S-6",
            "concept": "Algebra",
            "misconceptions": [{"label": "D", "rationale": "r", "confidence": 0.5}],
            "status": "ok",
        },
        {
            "student_id": "S-7",
            "concept": "Algebra",
            "misconceptions": [{"label": "C", "rationale": "r", "confidence": 0.5}],
            "status": "ok",
        },
    ]

    summary_first = build_cohort_summary(rows)
    summary_second = build_cohort_summary(rows)

    assert summary_first == summary_second
    assert [item["label"] for item in summary_first["Fractions"]] == ["B", "A"]

    first = summary_first["Fractions"][0]
    assert first["occurrences"] == 2
    assert first["affected_students"] == 2
    assert first["avg_confidence"] == 0.7

    assert [item["label"] for item in summary_first["Algebra"]] == ["C", "D"]


def test_report_json_is_deterministic(tmp_path) -> None:
    rows = [
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "student_answer": "2/6",
            "misconceptions": [{"label": "Denominator", "rationale": "r", "confidence": 0.8}],
            "status": "ok",
        },
        {
            "student_id": "S-2",
            "concept": "Fractions",
            "question_text": "1/3 + 1/6 = ?",
            "student_answer": "2/9",
            "misconceptions": [{"label": "Structure", "rationale": "r", "confidence": 0.5}],
            "status": "json_repaired",
        },
        {
            "student_id": "S-3",
            "concept": "Fractions",
            "question_text": "1/3 + 1/3 = ?",
            "student_answer": "2/6",
            "misconceptions": [],
            "status": "retry_exhausted",
        },
    ]

    report_one = build_teacher_report(rows)
    report_two = build_teacher_report(rows)
    assert report_one == report_two
    assert report_one["metadata"]["rows_excluded_retry_exhausted"] == 1

    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"

    write_teacher_report(report_one, str(first_path))
    write_teacher_report(report_two, str(second_path))

    assert first_path.read_text(encoding="utf-8") == second_path.read_text(encoding="utf-8")
