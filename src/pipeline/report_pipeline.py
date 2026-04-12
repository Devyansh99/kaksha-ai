from __future__ import annotations

from typing import Any

from src.pipeline.report_aggregation import (
    INCLUDED_STATUSES,
    aggregate_by_student_concept,
    build_cohort_summary,
)


def _sorted_identified_misconceptions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for item in items:
        label = str(item.get("label", ""))
        rationale = str(item.get("rationale", ""))
        key = (label, rationale)
        confidence = float(item.get("confidence", 0.0))

        existing = grouped.get(key)
        if existing is None or confidence > existing["confidence"]:
            grouped[key] = {
                "label": label,
                "rationale": rationale,
                "confidence": confidence,
                "evidence_snippets": [],
            }

    normalized = list(grouped.values())
    normalized.sort(key=lambda entry: (entry["label"], entry["rationale"], -entry["confidence"]))
    return normalized


def _row_contains_label(row: dict[str, Any], label: str) -> bool:
    for misconception in row.get("misconceptions", []):
        if isinstance(misconception, dict) and str(misconception.get("label", "")) == label:
            return True
    return False


def _collect_evidence_snippets(rows: list[dict[str, Any]], label: str) -> list[dict[str, str]]:
    snippets: list[dict[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()

    sorted_rows = sorted(
        rows,
        key=lambda row: (
            str(row.get("student_id", "")),
            str(row.get("concept", "")),
            str(row.get("question_text", "")),
            str(row.get("student_answer", "")),
        ),
    )

    for row in sorted_rows:
        if str(row.get("status", "")) not in INCLUDED_STATUSES:
            continue
        if not _row_contains_label(row, label):
            continue

        question_text = str(row.get("question_text", ""))
        student_answer = str(row.get("student_answer", ""))
        pair = (question_text, student_answer)

        if pair in seen_pairs:
            continue

        snippets.append(
            {
                "question_text": question_text,
                "student_answer": student_answer,
            }
        )
        seen_pairs.add(pair)

        if len(snippets) >= 3:
            break

    return snippets


def build_teacher_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    aggregated = aggregate_by_student_concept(rows)
    cohort_summary = build_cohort_summary(rows)
    included_rows = [row for row in rows if str(row.get("status", "")) in INCLUDED_STATUSES]

    students: dict[str, dict[str, dict[str, Any]]] = {}
    for student_id in sorted(aggregated["students"].keys()):
        concept_map: dict[str, dict[str, Any]] = {}
        for concept in sorted(aggregated["students"][student_id].keys()):
            concept_data = aggregated["students"][student_id][concept]
            source_rows = [
                row
                for row in concept_data.get("source_rows", [])
                if str(row.get("status", "")) in INCLUDED_STATUSES
            ]
            identified = _sorted_identified_misconceptions(
                concept_data.get("identified_misconceptions", [])
            )
            for item in identified:
                item["evidence_snippets"] = _collect_evidence_snippets(
                    source_rows,
                    item["label"],
                )

            concept_map[concept] = {
                "mastery_score": int(concept_data["mastery_score"]),
                "identified_misconceptions": identified,
            }
        students[student_id] = concept_map

    cohort: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for concept in sorted(cohort_summary.keys()):
        concept_rows = [row for row in included_rows if str(row.get("concept", "")) == concept]
        top_items: list[dict[str, Any]] = []
        for item in cohort_summary[concept]:
            label = str(item["label"])
            top_items.append(
                {
                    "label": label,
                    "occurrences": int(item["occurrences"]),
                    "affected_students": int(item["affected_students"]),
                    "avg_confidence": float(item["avg_confidence"]),
                    "evidence_snippets": _collect_evidence_snippets(concept_rows, label),
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
