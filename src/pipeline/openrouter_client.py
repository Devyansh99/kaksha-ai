from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib import request

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key: str
    model: str
    timeout_seconds: float = 30.0
    max_retries: int = 2
    backoff_seconds: float = 0.5
    temperature: float = 0.0
    max_tokens: int = 300


def load_openrouter_config() -> OpenRouterConfig:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    model = os.getenv("OPENROUTER_MODEL", "").strip()

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is required")
    if not model:
        model = "qwen/qwen3-235b-a22b:free"

    return OpenRouterConfig(api_key=api_key, model=model)


def build_request_payload(prompt: str, config: OpenRouterConfig) -> dict:
    return {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
    }


def _send_json_request(payload: dict, config: OpenRouterConfig) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        OPENROUTER_ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
        },
    )
    with request.urlopen(req, timeout=config.timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def call_openrouter(prompt: str, config: OpenRouterConfig) -> dict:
    payload = build_request_payload(prompt, config)
    return _send_json_request(payload, config)
