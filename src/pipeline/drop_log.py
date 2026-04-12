from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def summarize_drops(records: list[dict]) -> dict:
    reason_counts = Counter(record.get("reason_code", "unknown") for record in records)
    return {
        "dropped_rows": len(records),
        "reason_counts": dict(reason_counts),
    }


def write_drop_log(records: list[dict], output_path: str = "artifacts/drop_log.jsonl") -> str:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")

    return str(target)
