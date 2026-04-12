from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from src.pipeline.ingest import run_ingestion_from_rows
from src.pipeline.misconception_extractor import extract_for_incorrect_rows
from src.pipeline.openrouter_client import load_openrouter_config
from src.pipeline.report_pipeline import build_teacher_report
from src.pipeline.report_writer import write_teacher_report


def analyze_rows(rows: list[dict[str, Any]], artifacts_dir: str = "artifacts") -> dict[str, Any]:
    output_dir = Path(artifacts_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    drop_log_path = output_dir / "api_drop_log.jsonl"
    report_path = output_dir / "api_teacher_report.json"

    incorrect_rows, ingestion_summary = run_ingestion_from_rows(
        raw_rows=rows,
        drop_log_path=str(drop_log_path),
    )

    config = load_openrouter_config()
    analyzed_rows = extract_for_incorrect_rows(incorrect_rows, config)

    status_counts = Counter(str(row.get("status", "unknown")) for row in analyzed_rows)

    report = build_teacher_report(analyzed_rows)
    write_teacher_report(report, output_path=str(report_path))

    return {
        "ingestion_summary": ingestion_summary,
        "incorrect_rows_forwarded": len(incorrect_rows),
        "analyzed_rows": len(analyzed_rows),
        "analysis_status_counts": dict(status_counts),
        "drop_log_path": str(drop_log_path),
        "report_path": str(report_path),
        "report": report,
    }
