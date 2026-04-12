# Quick Start

## Run API Server
```powershell
cd d:\SEM_6\Kaksha
.\venv\Scripts\python -m src.api_server
```
Open browser: `http://127.0.0.1:8000`

## Input Format (Paste in Web UI)
```json
[
  {
    "student_id": "S-701",
    "subject": "Math",
    "concept": "Fractions",
    "question_text": "1/2 + 1/4 = ?",
    "correct_answer": "3/4",
    "student_answer": "2/6",
    "is_correct": false,
    "timestamp": "2026-04-12T10:30:00Z"
  },
  {
    "student_id": "S-702",
    "subject": "Math",
    "concept": "Fractions",
    "question_text": "1/3 + 1/6 = ?",
    "correct_answer": "1/2",
    "student_answer": "2/9",
    "is_correct": false,
    "timestamp": "2026-04-12T10:35:00Z"
  }
]
```
Click "Analyze" → Get teacher report with LLM-detected misconceptions.

## Run All Tests
```powershell
cd d:\SEM_6\Kaksha
.\venv\Scripts\python -m pytest tests/ -v
```
Result: **23/23 tests passing** ✅

## Output
- Student misconceptions with confidence scores
- Mastery scores (0-100%)
- Cohort summary with top misconceptions
- Drop log for malformed rows

## Taxonomy & Extensibility

**Why "Uncategorized"?**  
Misconceptions are categorized against a predefined taxonomy:
- "Additive error" → "Fractions" group
- "Sign error" → "Arithmetic" group
- etc.

**If LLM detects a new misconception** not in taxonomy → Shows as "Uncategorized" with full details intact.

**To add new categories,** edit `src/pipeline/taxonomy_normalization.py`:
```python
CANONICAL_LABELS: dict[str, str] = {
    "New misconception": "Subject group",  # ← Add here
}

ALIAS_TO_CANONICAL: dict[str, str] = {
    "variant of new misconception": "New misconception",  # ← Add aliases
}
```

## Bonus: Two Prompting Strategies ⭐

Pipeline compares:
1. **Zero-shot** (current): Just schema → LLM infers misconceptions freely
2. **Few-shot**: Schema + worked example → Better consistency

Both implemented in `src/pipeline/misconception_prompt.py`. Run with either via `strategy_comparison.py`.
