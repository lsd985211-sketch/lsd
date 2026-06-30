#!/usr/bin/env python3
"""Minimal MCP-style wrapper for the public seed system."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_system import bootstrap_context

ROOT = Path(os.getenv("PROJECT_KB_ROOT", os.getcwd())).resolve()
SUPPORTED_PROTOCOL_VERSIONS = {"2025-06-18", "2025-03-26", "2024-11-05"}
DEFAULT_PROTOCOL_VERSION = "2025-06-18"


def _text(content: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(content, ensure_ascii=False)}]}


def _files() -> list[Path]:
    ignored = {".git", "node_modules", "runtime", "logs", "backups", "__pycache__"}
    return sorted(p for p in ROOT.rglob("*.md") if p.is_file() and not any(part.casefold() in ignored for part in p.parts)) if ROOT.exists() else []


def kb_stats() -> dict[str, Any]:
    files = _files()
    return {"ok": True, "root": str(ROOT), "file_count": len(files), "total_bytes": sum(p.stat().st_size for p in files)}


def kb_search(args: dict[str, Any]) -> dict[str, Any]:
    query = str(args.get("query", "")).strip().casefold()
    if not query:
        return {"ok": False, "error": "query is required"}
    terms = [term for term in query.split() if term]
    matches = []
    for path in _files():
        text = path.read_text(encoding="utf-8", errors="replace")
        folded = text.casefold()
        score = sum(folded.count(term) for term in terms)
        if score > 0:
            matches.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "score": score})
    matches.sort(key=lambda item: item["score"], reverse=True)
    return {"ok": True, "matches": matches[: int(args.get("limit", 10))]}


def bootstrap_context_pack(args: dict[str, Any]) -> dict[str, Any]:
    parsed = argparse.Namespace(workspace=str(args.get("workspace") or ROOT), project_id=str(args.get("project_id", "") or ""), task=str(args.get("task", "") or ""), depth=str(args.get("depth", "normal") or "normal"), format="json" if args.get("json") else "markdown", checkpoint_limit=int(args.get("checkpoint_limit", 6)), snippet_chars=int(args.get("snippet_chars", 1200)))
    payload = bootstrap_context.build_payload(parsed)
    return {"ok": True, "tool": "bootstrap_context_pack", "read_only": True, "payload": payload if args.get("json") else bootstrap_context.render_markdown(payload)}


TOOLS = [
    {"name": "kb_stats", "description": "Summarize markdown files under PROJECT_KB_ROOT.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kb_search", "description": "Search markdown files by keyword.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["query"]}},
    {"name": "bootstrap_context_pack", "description": "Generate a read-only agent bootstrap context pack.", "inputSchema": {"type": "object", "properties": {"workspace": {"type": "string"}, "project_id": {"type": "string"}, "task": {"type": "string"}, "depth": {"type": "string", "enum": ["quick", "normal", "deep"], "default": "normal"}, "json": {"type": "boolean", "default": False}}}},
]


def handle(req: dict[str, Any]) -> dict[str, Any] | None:
    method = req.get("method")
    req_id = req.get("id")
    if method == "initialize":
        version = (req.get("params") or {}).get("protocolVersion")
        if version not in SUPPORTED_PROTOCOL_VERSIONS:
            version = DEFAULT_PROTOCOL_VERSION
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": {"name": "seed-system", "version": "0.1.0"}}}
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        result = kb_stats() if name == "kb_stats" else kb_search(args) if name == "kb_search" else bootstrap_context_pack(args) if name == "bootstrap_context_pack" else {"ok": False, "error": f"unknown tool: {name}"}
        return {"jsonrpc": "2.0", "id": req_id, "result": _text(result)}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"unknown method: {method}"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(json.dumps(handle(json.loads(line)), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
