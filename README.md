# Kaksha Misconception Analyzer

Small prototype that analyzes student answer logs, detects misconceptions with an LLM, and returns a teacher-facing report.

## Quick start

```powershell
cd d:\SEM_6\Kaksha
.\venv\Scripts\python -m src.api_server
```

Open `http://127.0.0.1:8000` and click **Analyze** in the web UI.

## Notes on multi-teacher editing

Current state: this app does **not** store or merge teacher annotations. The API is stateless, so concurrent requests are processed independently, and there is no profile-level locking, versioning, or conflict handling.

If I had more time: I would add persistent profile documents with optimistic concurrency (version numbers / ETags), audit history, and conflict-aware merge rules so two teachers editing the same student profile can resolve overlaps safely.

## Data fetching decisions

- I kept `/analyze` as a single end-to-end call because ingest, LLM extraction, and report aggregation are tightly coupled and are easiest to reason about as one pipeline run.
- In the UI, health check and analysis are separate concerns (`/health` and `/analyze`) so operational status can be checked independently of expensive analysis work.

## Extending SchoolConfig for subset visibility

There is no concrete `SchoolConfig` model in this prototype yet. I would extend it with role/group-scoped feature flags, for example:

```json
{
  "features": {
    "misconception_trends": { "enabled_for": ["teacher", "department_head"] },
    "cross_class_comparison": { "enabled_for": ["department_head"] }
  }
}
```

At request time, evaluate flags against teacher claims (role, department, permissions) and return only allowed fields/UI capabilities.