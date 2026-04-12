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
    monkeypatch.setenv("OPENROUTER_API_KEY", "demo-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b:free")

    config = load_openrouter_config()
    assert config.api_key == "demo-key"
    assert config.model == "qwen/qwen3-235b-a22b:free"

    prompt = "Return only valid JSON"
    payload = build_request_payload(prompt, config)
    assert payload["model"] == "qwen/qwen3-235b-a22b:free"
    assert payload["messages"][0]["content"] == prompt
    assert payload["temperature"] == config.temperature
    assert payload["max_tokens"] == config.max_tokens

    captured = {}

    def fake_send(req_payload: dict, req_config: OpenRouterConfig) -> dict:
        captured["payload"] = req_payload
        captured["config"] = req_config
        return {"id": "mock-response"}

    monkeypatch.setattr("src.pipeline.openrouter_client._send_json_request", fake_send)

    response = call_openrouter(prompt, config)
    assert response["id"] == "mock-response"
    assert captured["config"].api_key == "demo-key"
    assert captured["payload"]["model"] == "qwen/qwen3-235b-a22b:free"
    assert captured["payload"]["messages"][0]["content"] == prompt
