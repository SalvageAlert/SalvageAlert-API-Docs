"""A tiny, dependency-free client: auth, JSON, typed errors and retry on 429/5xx."""
import json
import os
import time
import urllib.error
import urllib.request

BASE = "https://salvagealert.com/api/v1"


class SalvageAlertError(Exception):
    def __init__(self, status, body):
        err = (body or {}).get("error", {})
        super().__init__(f"{status} {err.get('code')}: {err.get('message')}")
        self.status = status
        self.code = err.get("code")
        self.request_id = (body or {}).get("request_id")
        self.body = body


def call(method, path, body=None, key=None, max_retries=4):
    """Return (data, headers). Raises SalvageAlertError on a non-2xx."""
    key = key or os.environ.get("SALVAGEALERT_KEY")
    if not key:
        raise RuntimeError("Set SALVAGEALERT_KEY")
    headers = {"Authorization": f"Bearer {key}", "User-Agent": "salvagealert-example/1.0"}
    payload = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(body).encode()

    for attempt in range(max_retries + 1):
        req = urllib.request.Request(BASE + path, data=payload, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                return json.load(res), dict(res.headers)
        except urllib.error.HTTPError as e:
            try:
                err_body = json.load(e)
            except Exception:
                err_body = None
            retryable = e.code == 429 or e.code >= 500
            if not retryable or attempt == max_retries:
                raise SalvageAlertError(e.code, err_body) from None
            wait = float(e.headers.get("Retry-After", 1)) if e.code == 429 else min(60, 2 ** attempt)
            time.sleep(wait)
