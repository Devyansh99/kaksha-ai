from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib import request

GEMINI_ENDPOINT_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
)


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    model: str
    timeout_seconds: float = 30.0
    max_retries: int = 2
    backoff_seconds: float = 0.5
    temperature: float = 0.0
    max_tokens: int = 300


def _load_env_file() -> dict:
    """Load variables from .env file in project root."""
    env_file = Path(__file__).parent.parent.parent / ".env"
    env_vars = {}

    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()
    
    return env_vars


def _normalize_gemini_model(value: str) -> str:
    model = value.strip()
    if model.startswith("models/"):
        return model.split("models/", 1)[1]
    return model


def load_llm_config() -> LLMConfig:
    """Load Gemini configuration from .env or process environment."""
    env_vars = _load_env_file()

    gemini_api_key = (
        env_vars.get("GEMINI_API_KEY", "").strip()
        or os.getenv("GEMINI_API_KEY", "").strip()
        or env_vars.get("OPENROUTER_API_KEY", "").strip()
        or os.getenv("OPENROUTER_API_KEY", "").strip()
    )
    gemini_model = (
        env_vars.get("GEMINI_MODEL", "").strip()
        or os.getenv("GEMINI_MODEL", "").strip()
        or env_vars.get("OPENROUTER_MODEL", "").strip()
        or os.getenv("OPENROUTER_MODEL", "").strip()
    )

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is required in .env file or GEMINI_API_KEY env var")

    model = _normalize_gemini_model(gemini_model) or "gemini-2.0-flash"
    return LLMConfig(api_key=gemini_api_key, model=model)


def load_openrouter_config() -> LLMConfig:
    """Backward-compatible alias kept for existing imports/tests."""
    return load_llm_config()


def build_request_payload(prompt: str, config: LLMConfig) -> dict:
    return {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": config.temperature,
            "maxOutputTokens": config.max_tokens,
        },
    }


def _send_json_request(payload: dict, config: LLMConfig) -> dict:
    body = json.dumps(payload).encode("utf-8")
    endpoint = GEMINI_ENDPOINT_TEMPLATE.format(model=config.model, api_key=config.api_key)
    req = request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=config.timeout_seconds) as response:
            raw_response = json.loads(response.read().decode("utf-8"))
            text_parts: list[str] = []
            for candidate in raw_response.get("candidates", []):
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(str(part.get("text", "")))

            return {
                "choices": [
                    {
                        "message": {
                            "content": "".join(text_parts),
                        }
                    }
                ],
                "provider_raw": raw_response,
            }
    except Exception as e:
        print(f"DEBUG: API Error - {type(e).__name__}: {e}")
        if hasattr(e, "read"):
            try:
                error_body = e.read().decode("utf-8")
                print(f"DEBUG: Error Response: {error_body}")
            except Exception:
                pass
        raise


def call_llm(prompt: str, config: LLMConfig) -> dict:
    payload = build_request_payload(prompt, config)
    return _send_json_request(payload, config)


def call_openrouter(prompt: str, config: LLMConfig) -> dict:
    """Backward-compatible alias kept for existing imports/tests."""
    return call_llm(prompt, config)


# Backward-compatible alias kept for existing imports/tests.
OpenRouterConfig = LLMConfig
