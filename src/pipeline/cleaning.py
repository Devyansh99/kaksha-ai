from __future__ import annotations

from datetime import datetime, timezone

from src.pipeline.contracts import validate_row_contract


def normalize_timestamp(raw_timestamp: str) -> tuple[str | None, str | None]:
    candidate = raw_timestamp.strip()
    if not candidate:
        return None, "invalid_timestamp"

    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S"):
            try:
                parsed = datetime.strptime(raw_timestamp, fmt)
                break
            except ValueError:
                parsed = None
        if parsed is None:
            return None, "invalid_timestamp"

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)

    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ"), None


def clean_row(row: dict) -> tuple[dict | None, str | None]:
    is_valid, reason = validate_row_contract(row)
    if not is_valid:
        return None, reason

    normalized_timestamp, ts_reason = normalize_timestamp(row["timestamp"])
    if normalized_timestamp is None:
        return None, ts_reason

    cleaned = dict(row)
    cleaned["timestamp"] = normalized_timestamp
    return cleaned, None