"""Minimal webhook receiver that verifies X-Salvagealert-Signature.

Usage: SALVAGEALERT_WEBHOOK_SECRET=... python webhook_server.py   (listens on :8787)
"""
import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ["SALVAGEALERT_WEBHOOK_SECRET"]
seen = set()  # use a database in production, keyed on the delivery id


def verify(raw: bytes, header: str, secret: str, tolerance: int = 300) -> bool:
    if not header:
        return False
    parts = dict(p.strip().split("=", 1) for p in header.split(","))
    try:
        t = int(parts["t"])
    except (KeyError, ValueError):
        return False
    if abs(time.time() - t) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{t}.".encode() + raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, parts.get("v1", ""))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))  # RAW body
        if not verify(raw, self.headers.get("X-Salvagealert-Signature"), SECRET):
            self.send_response(401); self.end_headers(); return
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

        delivery_id = self.headers.get("X-Salvagealert-Delivery-Id")
        if delivery_id in seen:  # deliveries can repeat
            return
        seen.add(delivery_id)
        body = json.loads(raw)
        data = body["data"]
        if data["kind"] == "watch_match":
            lot = data["lot"]
            print(f"[{body['event']}] {lot['year']} {lot['make']} {lot['model']} {lot.get('detailUrl')}")
        else:
            print(f"[{body['event']}] {data['kind']}")


HTTPServer(("", 8787), Handler).serve_forever()
