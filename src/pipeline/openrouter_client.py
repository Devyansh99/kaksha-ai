from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
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


def load_openrouter_config() -> OpenRouterConfig:
    # Load from .env file first, then fallback to environment variables
    env_vars = _load_env_file()
    
    api_key = env_vars.get("OPENROUTER_API_KEY", "").strip() or os.getenv("OPENROUTER_API_KEY", "").strip()
    model = env_vars.get("OPENROUTER_MODEL", "").strip() or os.getenv("OPENROUTER_MODEL", "").strip()

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is required in .env file or OPENROUTER_API_KEY env var")
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
    try:
        with request.urlopen(req, timeout=config.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"DEBUG: API Error - {type(e).__name__}: {e}")
        if hasattr(e, 'read'):
            try:
                error_body = e.read().decode('utf-8')
                print(f"DEBUG: Error Response: {error_body}")
            except:
                pass
        raise


def call_openrouter(prompt: str, config: OpenRouterConfig) -> dict:
    payload = build_request_payload(prompt, config)
    return _send_json_request(payload, config)
