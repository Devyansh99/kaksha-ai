from __future__ import annotations

from collections import defaultdict
from typing import Any

INCLUDED_STATUSES = {"ok", "json_repaired", "fallback_used"}
EXCLUDED_STATUS = "retry_exhausted"


def _to_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence


def _iter_misconceptions(record: dict[str, Any]) -> list[dict[str, Any]]:
    misconceptions = record.get("misconceptions", [])
    if not isinstance(misconceptions, list):
        return []
    return [item for item in misconceptions if isinstance(item, dict)]


def _cohort_sort_key(item: dict[str, Any]) -> tuple[int, float, str]:
    return (-item["occurrences"], -item["avg_confidence"], item["label"])


def compute_mastery_score(records: list[dict[str, Any]]) -> int:
    if not records:
        return 100

    total_penalty = 0.0
    for record in records:
        for misconception in _iter_misconceptions(record):
            confidence = _to_confidence(misconception.get("confidence", 0.0))
            total_penalty += confidence * 25.0

    bounded_score = max(0.0, min(100.0, 100.0 - total_penalty))
    return int(round(bounded_score))


def aggregate_by_student_concept(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped_rows: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    excluded_retry_exhausted = 0

    for row in rows:
        status = str(row.get("status", ""))
        if status == EXCLUDED_STATUS:
            excluded_retry_exhausted += 1
            continue
        if status not in INCLUDED_STATUSES:
            continue

        student_id = str(row.get("student_id", ""))
        concept = str(row.get("concept", ""))
        grouped_rows[(student_id, concept)].append(row)

    students: dict[str, dict[str, dict[str, Any]]] = {}
    rows_included = 0

    for student_id, concept in sorted(grouped_rows.keys()):
        records = grouped_rows[(student_id, concept)]
        rows_included += len(records)

        student_bucket = students.setdefault(student_id, {})
        student_bucket[concept] = {
            "mastery_score": compute_mastery_score(records),
            "rows_considered": len(records),
            "identified_misconceptions": [
                {
                    "label": str(item.get("label", "")),
                    "rationale": str(item.get("rationale", "")),
                    "confidence": _to_confidence(item.get("confidence", 0.0)),
                }
                for record in records
                for item in _iter_misconceptions(record)
            ],
            "source_rows": records,
        }

    return {
        "students": students,
        "metadata": {
            "total_rows_processed": len(rows),
            "rows_included": rows_included,
            "rows_excluded_retry_exhausted": excluded_retry_exhausted,
        },
    }


def build_cohort_summary(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    concept_bucket: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)

    for row in rows:
        status = str(row.get("status", ""))
        if status not in INCLUDED_STATUSES:
            continue

        concept = str(row.get("concept", ""))
        student_id = str(row.get("student_id", ""))

        for misconception in _iter_misconceptions(row):
            label = str(misconception.get("label", ""))
            if label == "":
                continue

            entry = concept_bucket[concept].setdefault(
                label,
                {
                    "label": label,
                    "occurrences": 0,
                    "affected_students": set(),
                    "confidence_total": 0.0,
                },
            )
            confidence = _to_confidence(misconception.get("confidence", 0.0))
            entry["occurrences"] += 1
            entry["affected_students"].add(student_id)
            entry["confidence_total"] += confidence

    cohort_summary: dict[str, list[dict[str, Any]]] = {}
    for concept in sorted(concept_bucket.keys()):
        entries: list[dict[str, Any]] = []
        for label, bucket in concept_bucket[concept].items():
            occurrences = int(bucket["occurrences"])
            avg_confidence = 0.0
            if occurrences > 0:
                avg_confidence = round(bucket["confidence_total"] / occurrences, 4)

            entries.append(
                {
                    "label": label,
                    "occurrences": occurrences,
                    "affected_students": len(bucket["affected_students"]),
                    "avg_confidence": avg_confidence,
                }
            )

        entries.sort(key=_cohort_sort_key)
        cohort_summary[concept] = entries

    return cohort_summary
