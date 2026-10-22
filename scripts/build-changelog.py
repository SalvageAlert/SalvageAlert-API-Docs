"""Render CHANGELOG.md from the spec's x-changelog array."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "openapi/openapi.json").read_text())
lines = [
    "# Changelog",
    "",
    "Generated from `x-changelog` in [`openapi/openapi.json`](openapi/openapi.json). Newest first.",
    "Additive changes bump the minor version; nothing in v1 is ever removed. See [conventions](docs/conventions.md#versioning).",
    "",
]
for entry in spec.get("x-changelog", []):
    lines.append(f"## {entry['version']} — {entry['date']}")
    lines.append("")
    lines += [f"- {c}" for c in entry.get("changes", [])]
    lines.append("")
(ROOT / "CHANGELOG.md").write_text("\n".join(lines))
print(f"wrote CHANGELOG.md: {len(spec.get('x-changelog', []))} versions")
