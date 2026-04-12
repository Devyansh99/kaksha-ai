from src.pipeline.report_aggregation import aggregate_by_student_concept, compute_mastery_score


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
