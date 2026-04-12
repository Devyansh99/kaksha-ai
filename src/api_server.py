from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from src.pipeline.service import analyze_rows


class PipelineAPIHandler(BaseHTTPRequestHandler):
    WEB_INDEX_PATH = Path(__file__).resolve().parent / "web" / "index.html"

    def _send_json(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            if not self.WEB_INDEX_PATH.exists():
                self._send_json(500, {"error": "web_page_missing"})
                return
            html = self.WEB_INDEX_PATH.read_text(encoding="utf-8")
            self._send_html(200, html)
            return
        if self.path == "/health":
            self._send_json(200, {"ok": True})
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/analyze":
            self._send_json(404, {"error": "not_found"})
            return

        try:
            raw_len = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "invalid_content_length"})
            return

        try:
            body = self.rfile.read(raw_len)
            payload = json.loads(body.decode("utf-8"))
        except Exception:  # noqa: BLE001
            self._send_json(400, {"error": "invalid_json"})
            return

        rows: list[dict[str, Any]]
        if isinstance(payload, list):
            rows = [item for item in payload if isinstance(item, dict)]
        elif isinstance(payload, dict) and isinstance(payload.get("rows"), list):
            rows = [item for item in payload["rows"] if isinstance(item, dict)]
        else:
            self._send_json(400, {"error": "expected_rows_list"})
            return

        try:
            result = analyze_rows(rows)
            self._send_json(200, result)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:  # noqa: BLE001
            self._send_json(500, {"error": f"internal_error: {type(exc).__name__}"})


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), PipelineAPIHandler)
    print(f"Pipeline API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
