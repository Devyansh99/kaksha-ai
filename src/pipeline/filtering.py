from __future__ import annotations


def validate_is_correct(value) -> tuple[bool, str | None]:
    if not isinstance(value, bool):
        return False, "invalid_is_correct"
    return True, None


def filter_incorrect_rows(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    forwarded: list[dict] = []
    dropped: list[dict] = []

    for idx, row in enumerate(rows):
        is_valid, reason = validate_is_correct(row.get("is_correct"))
        if not is_valid:
            dropped.append(
                {
                    "row_index": idx,
                    "reason_code": reason,
                    "field": "is_correct",
                    "row": row,
                }
            )
            continue

        if row["is_correct"] is False:
            forwarded.append(row)

    return forwarded, dropped