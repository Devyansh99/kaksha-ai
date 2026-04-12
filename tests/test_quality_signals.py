from src.pipeline.taxonomy_normalization import normalize_label
from src.pipeline.report_pipeline import build_teacher_report


def test_normalize_label_maps_aliases_deterministically() -> None:
    alias = normalize_label("added denominators")
    assert alias["raw_label"] == "added denominators"
    assert alias["normalized_label"] == "Denominator addition"
    assert alias["taxonomy_group"] == "Fractions"
    assert alias["normalization_reason"] == "alias_match"

    unknown = normalize_label("completely unknown misconception")
    assert unknown["normalized_label"] == "Uncategorized"
    assert unknown["taxonomy_group"] == "Uncategorized"
    assert unknown["normalization_reason"] == "no_taxonomy_match"


def test_report_includes_normalized_labels_and_confidence_bands() -> None:
    rows = [
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "Q1",
            "student_answer": "A1",
            "misconceptions": [
                {"label": "added denominators", "rationale": "r1", "confidence": 0.39},
            ],
            "status": "ok",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "Q2",
            "student_answer": "A2",
            "misconceptions": [
                {"label": "structure", "rationale": "r2", "confidence": 0.40},
            ],
            "status": "json_repaired",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "Q3",
            "student_answer": "A3",
            "misconceptions": [
                {"label": "Reduction", "rationale": "r3", "confidence": 0.74},
            ],
            "status": "fallback_used",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "Q4",
            "student_answer": "A4",
            "misconceptions": [
                {"label": "Sign error", "rationale": "r4", "confidence": 0.75},
            ],
            "status": "ok",
        },
        {
            "student_id": "S-1",
            "concept": "Fractions",
            "question_text": "Q5",
            "student_answer": "A5",
            "misconceptions": [
                {"label": "added denominators", "rationale": "r5", "confidence": 1.0},
            ],
            "status": "retry_exhausted",
        },
    ]

    report = build_teacher_report(rows)
    identified = report["students"]["S-1"]["Fractions"]["identified_misconceptions"]

    by_confidence = {item["confidence_rounded"]: item for item in identified}
    assert by_confidence[0.39]["confidence_band"] == "low"
    assert by_confidence[0.4]["confidence_band"] == "medium"
    assert by_confidence[0.74]["confidence_band"] == "medium"
    assert by_confidence[0.75]["confidence_band"] == "high"

    for item in identified:
        assert "raw_label" in item
        assert "normalized_label" in item
        assert "taxonomy_group" in item
        assert "normalization_reason" in item

    cohort = report["cohort_summary"]["Fractions"]["top_misconceptions"]
    assert all("confidence_band" in item for item in cohort)
    assert all("avg_confidence_rounded" in item for item in cohort)
    assert report["metadata"]["rows_excluded_retry_exhausted"] == 1
