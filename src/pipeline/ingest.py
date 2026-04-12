from __future__ import annotations

import json
from pathlib import Path

from src.pipeline.cleaning import clean_row
from src.pipeline.drop_log import summarize_drops, write_drop_log
from src.pipeline.filtering import filter_incorrect_rows

REASON_FIELD_MAP = {
    "missing_required_field": "required_field",
    "invalid_field_type": "required_field",
    "invalid_timestamp": "timestamp",
}


def run_ingestion_from_rows(
    raw_rows: list[dict], drop_log_path: str = "artifacts/drop_log.jsonl"
) -> tuple[list[dict], dict]:
    cleaned_rows: list[dict] = []
    dropped_rows: list[dict] = []

    for idx, raw_row in enumerate(raw_rows):
        cleaned, reason = clean_row(raw_row)
        if cleaned is None:
            dropped_rows.append(
                {
                    "row_index": idx,
                    "reason_code": reason,
                    "field": REASON_FIELD_MAP.get(reason, "unknown"),
                    "row": raw_row,
                }
            )
            continue
        cleaned_rows.append(cleaned)

    incorrect_rows, filter_drops = filter_incorrect_rows(cleaned_rows)

    drop_offset = len(raw_rows)
    for filter_drop in filter_drops:
        drop_record = dict(filter_drop)
        drop_record["row_index"] = drop_offset + int(drop_record["row_index"])
        dropped_rows.append(drop_record)

    write_drop_log(dropped_rows, output_path=drop_log_path)
    drop_summary = summarize_drops(dropped_rows)

    summary = {
        "total_rows": len(raw_rows),
        "valid_rows": len(cleaned_rows),
        "dropped_rows": drop_summary["dropped_rows"],
        "reason_counts": drop_summary["reason_counts"],
    }

    print(json.dumps(summary, sort_keys=True))
    return incorrect_rows, summary


def run_ingestion_pipeline(
    input_path: str, drop_log_path: str = "artifacts/drop_log.jsonl"
) -> tuple[list[dict], dict]:
    raw_rows = json.loads(Path(input_path).read_text(encoding="utf-8"))
    return run_ingestion_from_rows(raw_rows=raw_rows, drop_log_path=drop_log_path)
