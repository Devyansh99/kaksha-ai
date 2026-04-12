from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.pipeline.misconception_prompt import (
    build_misconception_prompt_few_shot,
    build_misconception_prompt_zero_shot,
)
from src.pipeline.report_aggregation import INCLUDED_STATUSES
from src.pipeline.taxonomy_normalization import normalize_label

Analyzer = Callable[[str, dict[str, Any]], dict[str, Any]]


def _sorted_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("student_id", "")),
            str(row.get("concept", "")),
            str(row.get("question_text", "")),
            str(row.get("student_answer", "")),
        ),
    )


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


def _normalized_labels(result: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    misconceptions = result.get("misconceptions", [])
    if not isinstance(misconceptions, list):
        return labels

    for item in misconceptions:
        if not isinstance(item, dict):
            continue
        raw_label = str(item.get("label", ""))
        normalized_label = normalize_label(raw_label).get("normalized_label", "Uncategorized")
        labels.append(str(normalized_label))

    labels.sort()
    return labels


def _signature(row: dict[str, Any], result: dict[str, Any]) -> tuple[str, str, str, tuple[str, ...], str]:
    return (
        str(row.get("student_id", "")),
        str(row.get("concept", "")),
        str(row.get("question_text", "")),
        tuple(_normalized_labels(result)),
        str(result.get("status", "")),
    )


def _evaluate_strategy(
    rows: list[dict[str, Any]],
    prompt_builder: Callable[[dict[str, Any]], str],
    analyzer: Analyzer,
) -> dict[str, float]:
    parse_successes = 0
    normalized_label_hits = 0
    total_labels = 0
    confidence_values: list[float] = []

    first_run_signatures: list[tuple[str, str, str, tuple[str, ...], str]] = []

    for row in rows:
        result = analyzer(prompt_builder(row), row)
        status = str(result.get("status", ""))

        if status in INCLUDED_STATUSES:
            parse_successes += 1

        labels = _normalized_labels(result)
        for label in labels:
            total_labels += 1
            if label != "Uncategorized":
                normalized_label_hits += 1

        misconceptions = result.get("misconceptions", [])
        if isinstance(misconceptions, list):
            for item in misconceptions:
                if isinstance(item, dict):
                    confidence_values.append(_to_confidence(item.get("confidence", 0.0)))

        first_run_signatures.append(_signature(row, result))

    second_run_signatures: list[tuple[str, str, str, tuple[str, ...], str]] = []
    for row in rows:
        result = analyzer(prompt_builder(row), row)
        second_run_signatures.append(_signature(row, result))

    rows_count = len(rows)
    matching_signatures = sum(
        1 for first, second in zip(first_run_signatures, second_run_signatures) if first == second
    )

    parse_success_rate = 1.0 if rows_count == 0 else parse_successes / rows_count
    normalized_label_coverage = 0.0 if total_labels == 0 else normalized_label_hits / total_labels
    rerun_consistency = 1.0 if rows_count == 0 else matching_signatures / rows_count
    avg_confidence = 0.0 if not confidence_values else sum(confidence_values) / len(confidence_values)

    return {
        "parse_success_rate": round(parse_success_rate, 4),
        "normalized_label_coverage": round(normalized_label_coverage, 4),
        "rerun_consistency": round(rerun_consistency, 4),
        "avg_confidence": round(avg_confidence, 4),
    }


def compare_prompt_strategies(rows: list[dict[str, Any]], analyzer: Analyzer) -> dict[str, Any]:
    ordered_rows = _sorted_rows(rows)

    metrics = {
        "zero_shot": _evaluate_strategy(
            ordered_rows,
            prompt_builder=build_misconception_prompt_zero_shot,
            analyzer=analyzer,
        ),
        "few_shot": _evaluate_strategy(
            ordered_rows,
            prompt_builder=build_misconception_prompt_few_shot,
            analyzer=analyzer,
        ),
    }

    ranking = sorted(
        metrics.keys(),
        key=lambda strategy: (
            -metrics[strategy]["parse_success_rate"],
            -metrics[strategy]["normalized_label_coverage"],
            -metrics[strategy]["rerun_consistency"],
            -metrics[strategy]["avg_confidence"],
            strategy,
        ),
    )

    return {
        "rows_evaluated": len(ordered_rows),
        "metrics": metrics,
        "ranking": ranking,
    }


def write_strategy_summary(
    result: dict[str, Any],
    output_path: str = ".planning/phases/04-quality-signals-and-evaluation/04-AB-RESULTS.md",
) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    metrics = result.get("metrics", {})
    ranking = result.get("ranking", [])

    lines = [
        "# Phase 4 Prompt Strategy Comparison",
        "",
        f"Rows evaluated: {int(result.get('rows_evaluated', 0))}",
        "",
        "## Metrics",
        "",
        "| Strategy | parse_success_rate | normalized_label_coverage | rerun_consistency | avg_confidence |",
        "|----------|--------------------|---------------------------|-------------------|----------------|",
    ]

    for strategy in ("zero_shot", "few_shot"):
        strategy_metrics = metrics.get(strategy, {})
        lines.append(
            "| {strategy} | {parse_success_rate:.4f} | {normalized_label_coverage:.4f} | {rerun_consistency:.4f} | {avg_confidence:.4f} |".format(
                strategy=strategy,
                parse_success_rate=float(strategy_metrics.get("parse_success_rate", 0.0)),
                normalized_label_coverage=float(
                    strategy_metrics.get("normalized_label_coverage", 0.0)
                ),
                rerun_consistency=float(strategy_metrics.get("rerun_consistency", 0.0)),
                avg_confidence=float(strategy_metrics.get("avg_confidence", 0.0)),
            )
        )

    lines.extend(["", "## Ranking", ""])
    for index, strategy in enumerate(ranking, start=1):
        lines.append(f"{index}. {strategy}")

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
