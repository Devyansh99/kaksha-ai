# Technology Stack: Misconception Analyzer Pipeline

**Project:** Misconception Analyzer Pipeline  
**Scope:** Greenfield, local prototype (~4 hours), output `teacher_report.json`  
**Researched:** 2026-04-12

## Recommended Stack (2025-2026, Prototype-First)

### 1) Runtime and Environment

| Choice | Version | Why this choice | Confidence |
|---|---:|---|---|
| Python | `3.12.x` (recommended) | Best balance of modern features and library compatibility for a short prototype. | HIGH |
| Virtual env | `venv` (stdlib) | Zero setup overhead; ideal for fast local iteration. | HIGH |
| Package installer | `pip` (inside venv) | Ubiquitous and sufficient for a 4-hour prototype. | HIGH |

**Prescriptive note:** use Python `3.12.x` unless your machine already has a stable `3.11.x` setup. Do not spend prototype time migrating to newest interpreter features.

### 2) Core Data + Validation Layer

| Library | Version range | Purpose | Why this choice | Confidence |
|---|---:|---|---|---|
| `pandas` | `>=3.0,<3.1` | Load/clean `student_logs.json`, handle malformed rows | Standard for tabular cleaning and quick aggregation. | HIGH |
| `pydantic` | `>=2.12,<2.13` | Strict schemas for input rows and final report payload | Strong typed validation and serialization for JSON contracts. | HIGH |
| `orjson` | `>=3.11,<4` | Fast/strict JSON serialization | Useful for robust JSON I/O and deterministic output performance. | MEDIUM |

### 3) LLM Integration Layer

| Library/Service | Version range | Purpose | Why this choice | Confidence |
|---|---:|---|---|---|
| OpenRouter API | current | Model routing/provider for Qwen free model | Matches project constraint (Gemini quota exhausted). | HIGH |
| `openai` Python SDK | `>=2.31,<3` | Client wrapper with retries/timeouts and typed responses | OpenRouter supports OpenAI-compatible base URL flow; fastest path to implementation. | HIGH |
| `tenacity` | `>=9.1,<10` | Explicit retry/backoff around LLM calls | Adds resilient behavior for timeout/rate-limit/malformed response recovery. | HIGH |
| `python-dotenv` | `>=1.2,<2` | Local secrets/env loading | Simplifies API key handling without hardcoding credentials. | HIGH |

**Prescriptive integration approach:**
- Use `openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=...)`.
- Keep model configurable (default to your OpenRouter Qwen free model id).
- Request strict JSON output and validate with Pydantic before downstream aggregation.
- On validation failure, run one repair prompt; if still invalid, fallback to keyword heuristic.

### 4) CLI + Observability + Tests

| Library | Version range | Purpose | Why this choice | Confidence |
|---|---:|---|---|---|
| `typer` | `>=0.24,<0.25` | Simple CLI entrypoint (`analyze`) | Clean developer UX for local demo runs. | MEDIUM |
| `pytest` | `>=9.0,<10` | Minimal tests for parser, LLM parser, and report builder | Highest ROI testing for small prototype. | HIGH |
| `ruff` | `>=0.15,<0.16` | Lint + format | Fast single-tool quality gate for rapid iteration. | HIGH |

## Practical 4-Hour Build Profile

Use this trimmed install set first:

```bash
pip install "pandas>=3.0,<3.1" "pydantic>=2.12,<2.13" "openai>=2.31,<3" "tenacity>=9.1,<10" "python-dotenv>=1.2,<2"
pip install "pytest>=9.0,<10" "ruff>=0.15,<0.16"
```

Add only if needed:

```bash
pip install "orjson>=3.11,<4" "typer>=0.24,<0.25"
```

## Minimal Architecture for This Stack

1. `ingest.py`: read `student_logs.json`, normalize columns, mark/drop malformed rows with reason log.
2. `misconception_detector.py`: prompt builder + OpenRouter call + JSON parse/validate + retry/fallback.
3. `report_builder.py`: aggregate per student/per concept, compute mastery, attach misconceptions.
4. `main.py`: run pipeline and write `teacher_report.json`.

## What NOT to Use (Prototype Scope)

Avoid these for this milestone:

- `LangChain` / `LlamaIndex`: over-abstraction for one prompt pipeline; adds moving parts and debugging time.
- `FastAPI`/web backend: unnecessary because deliverable is a JSON file, not an API.
- Workflow orchestrators (`Airflow`, `Prefect`, `Dagster`): overhead exceeds value for single local batch run.
- Message brokers (`Kafka`, `RabbitMQ`) or task queues (`Celery`): no async/distributed requirement.
- Databases (`Postgres`, vector DBs): output is file-based JSON; DB setup is unnecessary complexity.
- Local LLM serving (`Ollama`, `vLLM`) for this task: setup time and hardware variance hurt 4-hour target.
- Heavy observability stacks (`OpenTelemetry`, Grafana) for prototype: replace with structured logs.

## Opinionated Default Settings

- LLM timeout: `20-30s` per call.
- Retries: max `2-3` with exponential backoff.
- Batch mode: process incorrect answers only (`is_correct == false`) for LLM stage.
- Report serialization: write once at end, UTF-8, stable key ordering.
- Failure policy: never crash whole run on one bad row or one bad LLM response.

## Confidence Summary

| Area | Level | Reason |
|---|---|---|
| Python runtime choice (`3.12`) | HIGH | Mature and stable for ecosystem dependencies in 2026. |
| Data + schema stack (`pandas` + `pydantic`) | HIGH | Dominant standard for Python data cleaning + strict JSON contracts. |
| LLM client stack (`openai` SDK with OpenRouter base URL) | HIGH | Official SDK + OpenRouter compatibility pattern documented. |
| Optional extras (`orjson`, `typer`) | MEDIUM | Good ROI but not strictly required for MVP success. |
| Exclusions (no orchestration/backend/db/vector stack) | HIGH | Directly aligned with 4-hour, local, single-output prototype goal. |

## Sources

- Python docs (3.14 page status and stable branches): https://docs.python.org/3/
- OpenRouter quickstart (OpenAI-compatible usage): https://openrouter.ai/docs/quickstart
- OpenAI Python SDK package/version and API behavior: https://pypi.org/project/openai/
- pandas docs and release line: https://pandas.pydata.org/docs/ , https://pypi.org/project/pandas/
- Pydantic docs/releases: https://docs.pydantic.dev/ , https://pypi.org/project/pydantic/
- tenacity: https://pypi.org/project/tenacity/
- python-dotenv: https://pypi.org/project/python-dotenv/
- orjson: https://pypi.org/project/orjson/
- ruff: https://pypi.org/project/ruff/
- pytest: https://pypi.org/project/pytest/
- typer: https://pypi.org/project/typer/
