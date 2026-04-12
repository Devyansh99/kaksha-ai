from __future__ import annotations

import time
from urllib.error import URLError

from src.pipeline.json_resilience import deterministic_keyword_fallback, parse_or_repair_json
from src.pipeline.misconception_prompt import build_misconception_prompt
from src.pipeline.openrouter_client import OpenRouterConfig, call_openrouter


def _extract_content(response: dict) -> str:
    choices = response.get("choices", [])
    if not choices:
        return ""

    first = choices[0]
    message = first.get("message", {})
    content = message.get("content", "")

    if isinstance(content, list):
        joined = []
        for item in content:
            if isinstance(item, dict):
                joined.append(str(item.get("text", "")))
            else:
                joined.append(str(item))
        return "".join(joined)

    return str(content)


def _base_record(row: dict) -> dict:
    return {
        "student_id": str(row.get("student_id", "")),
        "concept": str(row.get("concept", "")),
        "question_text": str(row.get("question_text", "")),
        "student_answer": str(row.get("student_answer", "")),
    }


def _retry_exhausted(row: dict, error_code: str) -> dict:
    record = _base_record(row)
    record.update(
        {
            "misconceptions": [],
            "source": "llm",
            "status": "retry_exhausted",
            "error_code": error_code,
        }
    )
    return record


def extract_misconceptions_for_row(row: dict, config: OpenRouterConfig) -> dict:
    prompt = build_misconception_prompt(row)
    attempt_limit = config.max_retries + 1

    for attempt in range(attempt_limit):
        try:
            response = call_openrouter(prompt, config)
        except TimeoutError:
            if attempt < config.max_retries:
                time.sleep(config.backoff_seconds * (attempt + 1))
                continue
            return _retry_exhausted(row, "timeout")
        except URLError:
            if attempt < config.max_retries:
                time.sleep(config.backoff_seconds * (attempt + 1))
                continue
            return _retry_exhausted(row, "service_error")
        except Exception:
            if attempt < config.max_retries:
                time.sleep(config.backoff_seconds * (attempt + 1))
                continue
            return _retry_exhausted(row, "service_error")

        parsed, status = parse_or_repair_json(_extract_content(response))
        if parsed is not None:
            record = _base_record(row)
            record["misconceptions"] = parsed.get("misconceptions", [])
            record["source"] = "llm"
            record["status"] = status
            record["error_code"] = None
            return record

        fallback = deterministic_keyword_fallback(row)
        fallback["error_code"] = "malformed_json"
        return fallback

    return _retry_exhausted(row, "service_error")


def extract_for_incorrect_rows(rows: list[dict], config: OpenRouterConfig) -> list[dict]:
    outputs: list[dict] = []
    for row in rows:
        outputs.append(extract_misconceptions_for_row(row, config))
    return outputs
