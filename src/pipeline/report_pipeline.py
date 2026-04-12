from __future__ import annotations

from typing import Any

from src.pipeline.report_aggregation import aggregate_by_student_concept, build_cohort_summary


def _sorted_identified_misconceptions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "label": str(item.get("label", "")),
                "rationale": str(item.get("rationale", "")),
                "confidence": float(item.get("confidence", 0.0)),
                "evidence_snippets": [],
            }
        )
    normalized.sort(key=lambda entry: (entry["label"], entry["rationale"], -entry["confidence"]))
    return normalized


def build_teacher_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    aggregated = aggregate_by_student_concept(rows)
    cohort_summary = build_cohort_summary(rows)

    students: dict[str, dict[str, dict[str, Any]]] = {}
    for student_id in sorted(aggregated["students"].keys()):
        concept_map: dict[str, dict[str, Any]] = {}
        for concept in sorted(aggregated["students"][student_id].keys()):
            concept_data = aggregated["students"][student_id][concept]
            concept_map[concept] = {
                "mastery_score": int(concept_data["mastery_score"]),
                "identified_misconceptions": _sorted_identified_misconceptions(
                    concept_data.get("identified_misconceptions", [])
                ),
            }
        students[student_id] = concept_map

    cohort: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for concept in sorted(cohort_summary.keys()):
        top_items: list[dict[str, Any]] = []
        for item in cohort_summary[concept]:
            top_items.append(
                {
                    "label": str(item["label"]),
                    "occurrences": int(item["occurrences"]),
                    "affected_students": int(item["affected_students"]),
                    "avg_confidence": float(item["avg_confidence"]),
                    "evidence_snippets": [],
                }
            )
        cohort[concept] = {"top_misconceptions": top_items}

    metadata = {
        "total_rows_processed": int(aggregated["metadata"]["total_rows_processed"]),
        "rows_included": int(aggregated["metadata"]["rows_included"]),
        "rows_excluded_retry_exhausted": int(
            aggregated["metadata"]["rows_excluded_retry_exhausted"]
        ),
        "generated_at": "deterministic",
    }

    return {
        "students": students,
        "cohort_summary": cohort,
        "metadata": metadata,
    }
