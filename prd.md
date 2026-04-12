Misconception Analyzer Pipeline
AI Engineer Intern — kaksha.ai Summer 2026

Effort

~4 hours

Type

Prototype

Stack

Python + LLM

Output

teacher_report.json

Goal

Build a lightweight Python pipeline that reads student Q&A logs, uses an LLM to identify specific misconceptions, and outputs an aggregated report for teachers.

Module 1 — Data processing

Input file: student_logs.json

Minimum 10 records. Include 1–2 intentionally malformed rows.

Schema (per record)

student_id, subject, concept, question_text, correct_answer, student_answer, is_correct, timestamp

Cleaning rules

Load into Pandas DataFrame. Handle missing fields, parse timestamps securely, drop malformed rows. Log what was dropped.

Module 2 — Misconception analysis (LLM)

2a
Prompt builder — takes one incorrect submission, returns a structured prompt that instructs the LLM to output only JSON (no hallucinations, strict format).
2b
Resilience — handle API timeouts, service errors, and malformed JSON returns gracefully.
2c
LLM backend — Gemini free tier or Ollama (local). API key must be substitutable via env var. If no API access, write a keyword-based mock and include the real prompts as comments.
2d ★
Bonus — implement and briefly compare two prompting strategies (e.g. zero-shot vs. few-shot, or a two-step chain).
Module 3 — Aggregation

Concept mastery score

0–100% per student per concept. Choose one approach: simple accuracy, time-weighted recency, or misconception-severity deduction.

Output: teacher_report.json

Keyed by student → concept → mastery_score + identified_misconceptions[ ]

Deliverables

GitHub repo

Public or private. Include README.md with local setup steps.

AI chat thread

Share public link or PDF of a chat where you pitch yourself for this role.

Code understanding

You must be able to explain every line — interviews will probe architecture and edge cases.

Success criteria

✓
Pipeline runs end-to-end on student_logs.json and produces valid teacher_report.json
✓
Malformed rows are caught and logged, not silently skipped or crashing
✓
LLM prompt enforces structured JSON output and handles failure modes
✓
Mastery score is thoughtful — not just raw accuracy