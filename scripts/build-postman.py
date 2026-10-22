"""Build postman/SalvageAlert.postman_collection.json from openapi/openapi.json.

Run after syncing the spec:  python3 scripts/build-postman.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "openapi/openapi.json").read_text())


def example_body(schema_ref):
    name = schema_ref.rsplit("/", 1)[-1]
    props = spec["components"]["schemas"].get(name, {}).get("properties", {})
    out = {}
    for k, v in props.items():
        if "example" in v:
            out[k] = v["example"]
        elif k == "source":
            out[k] = "copart_us"
    return out


folders = {}
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        if method not in ("get", "post", "patch", "put", "delete"):
            continue
        pm_path = re.sub(r"\{(\w+)\}", r":\1", path).strip("/").split("/")
        query = [
            {"key": p["name"], "value": str(p.get("example", "")), "disabled": not p.get("required", False),
             "description": (p.get("description") or "")[:300]}
            for p in op.get("parameters", []) if p.get("in") == "query"
        ]
        variables = [{"key": p["name"], "value": str(p.get("example", ""))}
                     for p in op.get("parameters", []) if p.get("in") == "path"]
        req = {
            "method": method.upper(),
            "header": [],
            "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": pm_path,
                    "query": query, "variable": variables},
            "description": op.get("description", ""),
        }
        rb = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        if "$ref" in rb:
            req["header"].append({"key": "Content-Type", "value": "application/json"})
            req["body"] = {"mode": "raw", "raw": json.dumps(example_body(rb["$ref"]), indent=2)}
        tag = (op.get("tags") or ["Other"])[0]
        folders.setdefault(tag, []).append({"name": f"{method.upper()} {path} · {op.get('summary', '')}", "request": req})

collection = {
    "info": {
        "name": f"SalvageAlert API v{spec['info']['version']}",
        "description": "Generated from https://salvagealert.com/api/v1/openapi.json. "
                       "Set the `apiKey` collection variable to your sa_live_ key (https://salvagealert.com/app/api).",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "{{apiKey}}", "type": "string"}]},
    "variable": [
        {"key": "baseUrl", "value": spec["servers"][0]["url"]},
        {"key": "apiKey", "value": "sa_live_REPLACE_ME"},
    ],
    "item": [{"name": t, "item": items} for t, items in folders.items()],
}
out = ROOT / "postman/SalvageAlert.postman_collection.json"
out.write_text(json.dumps(collection, indent=2) + "\n")
print(f"wrote {out.relative_to(ROOT)}: {sum(len(i) for i in folders.values())} requests in {len(folders)} folders")
