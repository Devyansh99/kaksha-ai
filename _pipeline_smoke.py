import json
import urllib.request

data = {
    "rows": [
        {
            "student_id": "S-701",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/2 + 1/4 = ?",
            "correct_answer": "3/4",
            "student_answer": "2/6",
            "is_correct": False,
            "timestamp": "2026-04-12T10:00:00Z"
        },
        {
            "student_id": "S-702",
            "subject": "Math",
            "concept": "Fractions",
            "question_text": "1/3 + 1/6 = ?",
            "correct_answer": "1/2",
            "student_answer": "2/9",
            "is_correct": False,
            "timestamp": "bad-date"
        }
    ]
}

body = json.dumps(data).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8000/analyze",
    data=body,
    method="POST",
    headers={"Content-Type": "application/json"},
)

with urllib.request.urlopen(req, timeout=120) as response:
    result = json.loads(response.read().decode("utf-8"))

print("STATUS_COUNTS", result.get("analysis_status_counts"))
print("ROWS_INCLUDED", result.get("report", {}).get("metadata", {}).get("rows_included"))
print("STUDENTS_KEYS", list(result.get("report", {}).get("students", {}).keys()))
