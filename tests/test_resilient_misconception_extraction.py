from src.pipeline.misconception_prompt import (
    REQUIRED_MISCONCEPTION_KEYS,
    REQUIRED_RESPONSE_KEYS,
    build_misconception_prompt,
)
from src.pipeline.openrouter_client import (
    OpenRouterConfig,
    build_request_payload,
    call_openrouter,
    load_openrouter_config,
)
from src.pipeline.json_resilience import (
    deterministic_keyword_fallback,
    parse_or_repair_json,
)
from src.pipeline.misconception_extractor import extract_misconceptions_for_row


def test_prompt_requires_json_only_contract() -> None:
    row = {
        "student_id": "S-100",
        "concept": "Fractions",
        "question_text": "1/3 + 1/6 = ?",
        "student_answer": "2/9",
    }

    prompt = build_misconception_prompt(row)

    assert "Return only valid JSON" in prompt
    assert all(key in prompt for key in REQUIRED_RESPONSE_KEYS)
    assert all(key in prompt for key in REQUIRED_MISCONCEPTION_KEYS)
    assert "markdown fences" in prompt


def test_openrouter_client_uses_env_config(monkeypatch) -> None:
    # Mock _load_env_file to return empty dict so environment variables are used
    monkeypatch.setattr("src.pipeline.openrouter_client._load_env_file", lambda: {})

    monkeypatch.setenv("GEMINI_API_KEY", "demo-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.0-flash")

    config = load_openrouter_config()
    assert config.api_key == "demo-key"
    assert config.model == "gemini-2.0-flash"

    prompt = "Return only valid JSON"
    payload = build_request_payload(prompt, config)
    assert payload["contents"][0]["parts"][0]["text"] == prompt
    assert payload["generationConfig"]["temperature"] == config.temperature
    assert payload["generationConfig"]["maxOutputTokens"] == config.max_tokens

    captured = {}

    def fake_send(req_payload: dict, req_config: OpenRouterConfig) -> dict:
        captured["payload"] = req_payload
        captured["config"] = req_config
        return {"id": "mock-response"}

    monkeypatch.setattr("src.pipeline.openrouter_client._send_json_request", fake_send)

    response = call_openrouter(prompt, config)
    assert response["id"] == "mock-response"
    assert captured["config"].api_key == "demo-key"
    assert captured["payload"]["contents"][0]["parts"][0]["text"] == prompt


def test_malformed_json_repair_then_fallback() -> None:
    repair_candidate = "```json\n{\"student_id\": \"S-1\", \"concept\": \"Fractions\",}\n```"
    repaired, repair_status = parse_or_repair_json(repair_candidate)

    assert repair_status == "json_repaired"
    assert repaired is not None
    assert repaired["student_id"] == "S-1"

    broken_payload = "this is not json"
    parsed, status = parse_or_repair_json(broken_payload)

    assert parsed is None
    assert status == "fallback_used"

    fallback = deterministic_keyword_fallback(
        {
            "student_id": "S-2",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "student_answer": "2/6",
        }
    )
    assert fallback["source"] == "fallback"
    assert fallback["status"] == "fallback_used"
    assert fallback["error_code"] is None
    assert all(
        key in fallback
        for key in (
            "student_id",
            "concept",
            "question_text",
            "student_answer",
            "misconceptions",
            "source",
            "status",
            "error_code",
        )
    )
    assert all(
        key in fallback["misconceptions"][0]
        for key in ("label", "rationale", "confidence")
    )


def test_retry_timeout_is_bounded_and_non_crashing(monkeypatch) -> None:
    attempts = {"count": 0}

    def always_timeout(prompt: str, config: OpenRouterConfig) -> dict:
        attempts["count"] += 1
        raise TimeoutError("simulated timeout")

    monkeypatch.setattr("src.pipeline.misconception_extractor.call_openrouter", always_timeout)
    monkeypatch.setattr("src.pipeline.misconception_extractor.time.sleep", lambda _sec: None)

    config = OpenRouterConfig(
        api_key="demo",
        model="qwen/qwen3-235b-a22b:free",
        timeout_seconds=0.01,
        max_retries=2,
        backoff_seconds=0.0,
    )

    output = extract_misconceptions_for_row(
        {
            "student_id": "S-9",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "student_answer": "2/6",
        },
        config,
    )

    assert attempts["count"] == 3
    assert output["source"] == "fallback"
    assert output["status"] == "fallback_used"
    assert output["error_code"] == "timeout"
    assert len(output["misconceptions"]) >= 1
