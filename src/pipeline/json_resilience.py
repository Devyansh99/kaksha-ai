from __future__ import annotations

import json
import re


def _strip_code_fences(raw_text: str) -> str:
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9_-]*\\n?", "", text)
        text = re.sub(r"\\n?```$", "", text)
    return text.strip()


def _remove_trailing_commas(raw_text: str) -> str:
    return re.sub(r",\s*([}\]])", r"\1", raw_text)


def _first_json_object(raw_text: str) -> str:
    start = raw_text.find("{")
    if start < 0:
        return raw_text

    depth = 0
    for index in range(start, len(raw_text)):
        char = raw_text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return raw_text[start : index + 1]
    return raw_text


def parse_or_repair_json(raw_text: str) -> tuple[dict | None, str]:
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            return parsed, "ok"
    except json.JSONDecodeError:
        pass

    repaired = _strip_code_fences(raw_text)
    repaired = _remove_trailing_commas(repaired)
    repaired = _first_json_object(repaired)

    try:
        parsed = json.loads(repaired)
        if isinstance(parsed, dict):
            return parsed, "json_repaired"
    except json.JSONDecodeError:
        pass

    return None, "fallback_used"


def deterministic_keyword_fallback(row: dict) -> dict:
    answer_text = str(row.get("student_answer", "")).lower()

    label = "General misconception"
    rationale = "Student answer deviates from expected concept pattern."

    if "2/6" in answer_text or "denominator" in answer_text:
        label = "Denominator addition misconception"
        rationale = "Student appears to add denominators directly in fraction addition."
    elif "2/9" in answer_text:
        label = "Fraction addition structure misconception"
        rationale = "Student output suggests incorrect numerator/denominator combination."

    return {
        "student_id": str(row.get("student_id", "")),
        "concept": str(row.get("concept", "")),
        "question_text": str(row.get("question_text", "")),
        "student_answer": str(row.get("student_answer", "")),
        "misconceptions": [
            {
                "label": label,
                "rationale": rationale,
                "confidence": 0.2,
            }
        ],
        "source": "fallback",
        "status": "fallback_used",
        "error_code": None,
    }
