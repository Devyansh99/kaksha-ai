from __future__ import annotations

import json


def write_teacher_report(report: dict, output_path: str = "teacher_report.json") -> None:
    payload = json.dumps(report, sort_keys=True, ensure_ascii=True, indent=2)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(payload)
        handle.write("\n")
