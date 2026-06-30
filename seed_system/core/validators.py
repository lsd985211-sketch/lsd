"""Lightweight validation helpers for public seed-system artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> tuple[bool, Any, str]:
    try:
        return True, json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:  # pragma: no cover - defensive CLI helper
        return False, None, str(exc)


def validate_public_artifacts(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    checks: list[dict[str, Any]] = []

    required_files = [
        "README.md",
        "VERSION.md",
        "CHANGELOG.md",
        "docs/public-api.md",
        "docs/architecture.md",
        "docs/architecture.schema.json",
        "docs/contracts/bootstrap-pack.schema.json",
        "docs/contracts/tool-catalog.schema.json",
        "docs/contracts/guardrails.schema.json",
        "examples/bootstrap-pack.example.json",
    ]
    for rel in required_files:
        checks.append({"name": f"file:{rel}", "ok": (root / rel).is_file()})

    ok, payload, error = _load_json(root / "examples/bootstrap-pack.example.json")
    checks.append({"name": "example_json_parse", "ok": ok, "error": error})
    if ok:
        checks.append({"name": "example_has_tool", "ok": isinstance(payload.get("tool"), dict)})
        checks.append({"name": "example_has_architecture", "ok": isinstance(payload.get("architecture"), dict)})
        checks.append({"name": "example_has_tool_knowledge", "ok": isinstance(payload.get("tool_knowledge"), dict)})
        checks.append({"name": "example_sanitized", "ok": "C:" not in json.dumps(payload)})

    return {"ok": all(item.get("ok") for item in checks), "checks": checks}

