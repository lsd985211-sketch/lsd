#!/usr/bin/env python3
"""Read-only bootstrap context pack generator for Codex/agent sessions."""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_VERSION = "0.1.0"
SENSITIVE_KEY_PARTS = ("token", "secret", "password", "authorization", "api_key", "apikey", "private_key")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists() or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if limit is not None and len(text) > limit:
        return text[:limit] + f"\n...[truncated {len(text) - limit} chars]"
    return text


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def sanitize_value(key: str, value: Any) -> Any:
    if any(part in key.casefold() for part in SENSITIVE_KEY_PARTS):
        return "[redacted]"
    if isinstance(value, dict):
        return {str(k): sanitize_value(str(k), v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_value(key, item) for item in value]
    if isinstance(value, str) and len(value) >= 24 and sum(ch.isalnum() for ch in value) / max(len(value), 1) > 0.85:
        return "[redacted]"
    return value


def summarize_config(workspace: Path) -> dict[str, Any]:
    project_config_path = workspace / ".codex" / "config.toml"
    global_config_path = Path.home() / ".codex" / "config.toml"
    project_config = load_toml(project_config_path)
    global_config = load_toml(global_config_path)
    return {
        "project_config_exists": project_config_path.exists(),
        "global_config_exists": global_config_path.exists(),
        "project_config_keys": sorted(project_config.keys()),
        "global_config_keys": sorted(global_config.keys()),
        "project_config_sanitized": sanitize_value("project_config", project_config),
    }


def checkpoint_manifest(workspace: Path) -> dict[str, Any]:
    candidates = [workspace / "_bridge" / "shared" / "checkpoints" / "MANIFEST.md", workspace / "checkpoints" / "MANIFEST.md"]
    for path in candidates:
        if path.exists():
            return {"path": str(path), "exists": True, "text": read_text(path, 6000)}
    return {"path": str(candidates[0]), "exists": False, "text": ""}


def recent_checkpoints(workspace: Path, project_id: str, limit: int, snippet_chars: int) -> list[dict[str, Any]]:
    roots = [workspace / "_bridge" / "shared" / "checkpoints", workspace / "checkpoints"]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        files.extend((root / project_id).glob("*.md") if project_id and (root / project_id).exists() else root.glob("*/*.md"))
    files = sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)
    return [{"path": str(p), "mtime": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(), "snippet": read_text(p, snippet_chars)} for p in files[:limit]]


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    workspace = Path(args.workspace).expanduser().resolve()
    agents_path = workspace / "AGENTS.md"
    return {
        "ok": workspace.exists(),
        "tool": {"name": "seed_system.bootstrap_context", "version": TOOL_VERSION, "schema": "bootstrap-pack-v1"},
        "generated_at": now_iso(),
        "workspace": str(workspace),
        "project_id": args.project_id,
        "task": args.task,
        "depth": args.depth,
        "rules": {
            "agents_md_exists": agents_path.exists(),
            "agents_md_path": str(agents_path),
            "agents_md_snippet": read_text(agents_path, args.snippet_chars) if args.depth in {"normal", "deep"} else "",
            "default_first_moves": [
                "Read local project instructions before editing.",
                "Treat memories and checkpoints as hints until live evidence confirms them.",
                "Verify drift-prone state such as ports, services, permissions, and tools before acting.",
            ],
        },
        "config": summarize_config(workspace) if args.depth in {"normal", "deep"} else {},
        "checkpoint_manifest": checkpoint_manifest(workspace),
        "recent_checkpoints": recent_checkpoints(workspace, args.project_id, args.checkpoint_limit, args.snippet_chars),
        "risk_sections": {
            "stable": ["project instructions", "checkpoint manifest", "bootstrap schema"],
            "live_verify": ["tool availability", "service state", "permissions", "current config drift"],
            "warnings": [] if workspace.exists() else ["workspace path does not exist"],
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Bootstrap Context Pack", "", f"- tool: `{payload['tool']['name']}` v`{payload['tool']['version']}`", f"- generated_at: `{payload['generated_at']}`", f"- workspace: `{payload['workspace']}`", f"- project_id: `{payload.get('project_id') or 'unspecified'}`", f"- task: {payload.get('task') or 'unspecified'}", f"- depth: `{payload['depth']}`", "", "## First Moves"]
    lines.extend(f"- {item}" for item in payload["rules"]["default_first_moves"])
    lines.extend(["", "## Project Instructions", f"- AGENTS.md exists: `{payload['rules']['agents_md_exists']}`"])
    manifest = payload.get("checkpoint_manifest") or {}
    lines.extend(["", "## Checkpoint Manifest", f"- exists: `{manifest.get('exists')}`", f"- path: `{manifest.get('path')}`"])
    lines.extend(["", "## Recent Checkpoints"])
    lines.extend(f"- `{item['path']}` ({item['mtime']})" for item in payload.get("recent_checkpoints") or [])
    if not payload.get("recent_checkpoints"):
        lines.append("- none")
    risks = payload.get("risk_sections") or {}
    lines.extend(["", "## Risk Sections"])
    for label in ("stable", "live_verify", "warnings"):
        values = risks.get(label) or []
        lines.append(f"- {label}:")
        if values:
            lines.extend(f"  - {value}" for value in values)
        else:
            lines.append("  - none")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a read-only bootstrap context pack.")
    parser.add_argument("--workspace", default=os.getcwd())
    parser.add_argument("--project-id", default="")
    parser.add_argument("--task", default="")
    parser.add_argument("--depth", choices=["quick", "normal", "deep"], default="normal")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--checkpoint-limit", type=int, default=6)
    parser.add_argument("--snippet-chars", type=int, default=1200)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = build_payload(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload), end="")
    return 0 if payload.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
