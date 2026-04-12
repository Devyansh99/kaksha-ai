# Misconception Analyzer Pipeline

**AI Engineer Intern — kaksha.ai Summer 2026**

| | |
|---|---|
| Effort | ~4 hours |
| Type | Prototype |
| Stack | Python + LLM |
| Output | `teacher_report.json` |

## Goal

Build a lightweight Python pipeline that reads student Q&A logs, uses an LLM to identify specific misconceptions, and outputs an aggregated report for teachers.

## Module 1 — Data Processing

**Input file:** `student_logs.json`
- Minimum 10 records
- Include 1–2 intentionally malformed rows

### Schema (per record)

```
student_id, subject, concept, question_text, correct_answer, student_answer, is_correct, timestamp
```

### Cleaning Rules

- Load into Pandas DataFrame
- Handle missing fields
- Parse timestamps securely
- Drop malformed rows
- Log what was dropped

## Module 2 — Misconception Analysis (LLM)

**2a — Prompt Builder**
- Takes one incorrect submission
- Returns a structured prompt that instructs the LLM to output only JSON (no hallucinations, strict format)

**2b — Resilience**
- Handle API timeouts, service errors, and malformed JSON returns gracefully

**2c — LLM Backend**
- OpenRouter Qwen 3.6 free model (cloud)
- Reason for switch: Gemini daily API request quota is exhausted today, so OpenRouter Qwen 3.6 free is being used instead
- API key must be substitutable via env var
- If no API access, write a keyword-based mock and include the real prompts as comments

**2d — Bonus ⭐**
- Implement and briefly compare two prompting strategies (e.g., zero-shot vs. few-shot, or a two-step chain)

## Module 3 — Aggregation

### Concept Mastery Score

- **Range:** 0–100% per student per concept
- **Approach:** Choose one: simple accuracy, time-weighted recency, or misconception-severity deduction

### Output: `teacher_report.json`

Keyed by `student → concept → mastery_score + identified_misconceptions[]`

## Deliverables

- **GitHub repo**
  - Public or private
  - Include `README.md` with local setup steps

- **AI chat thread**
  - Share public link or PDF of a chat where you pitch yourself for this role

- **Code understanding**
  - You must be able to explain every line — interviews will probe architecture and edge cases

## Success Criteria

- ✓ Pipeline runs end-to-end on `student_logs.json` and produces valid `teacher_report.json`
- ✓ Malformed rows are caught and logged, not silently skipped or crashing
- ✓ LLM prompt enforces structured JSON output and handles failure modes
- ✓ Mastery score is thoughtful — not just raw accuracy

$env:OPENROUTER_API_KEY="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"

$env:OPENROUTER_MODEL="qwen/qwen3-coder:free"

$env:PYTHONPATH="."

venv\Scripts\python -m src.api_server