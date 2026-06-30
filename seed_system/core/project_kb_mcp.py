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

from seed_system.core import bootstrap_context
from seed_system.core.architecture_contract import get_architecture_contract
from seed_system.core.guardrails import get_guardrails
from seed_system.core.tool_knowledge import get_tool_knowledge
from seed_system.core.tool_catalog import get_tool_catalog
from seed_system.core.validators import validate_public_artifacts

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


def architecture_contract(args: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "tool": "architecture_contract", "read_only": True, "payload": get_architecture_contract()}


def maintenance_contract(args: dict[str, Any]) -> dict[str, Any]:
    contract = get_architecture_contract().get("maintenance_contract", {})
    return {"ok": True, "tool": "maintenance_contract", "read_only": True, "payload": contract}


def capability_index(args: dict[str, Any]) -> dict[str, Any]:
    contract = get_architecture_contract().get("capability_index", {})
    return {"ok": True, "tool": "capability_index", "read_only": True, "payload": contract}


def agent_capabilities(args: dict[str, Any]) -> dict[str, Any]:
    contract = get_architecture_contract().get("capability_index", {})
    capabilities = []
    for section in contract.get("sections", []):
        if section.get("name") == "agent_capabilities":
            capabilities = section.get("entrypoints", [])
            break
    return {"ok": True, "tool": "agent_capabilities", "read_only": True, "payload": {"capabilities": capabilities}}


def growth_model(args: dict[str, Any]) -> dict[str, Any]:
    contract = get_architecture_contract().get("growth_model", {})
    return {"ok": True, "tool": "growth_model", "read_only": True, "payload": contract}


def agent_primitives(args: dict[str, Any]) -> dict[str, Any]:
    contract = get_architecture_contract().get("agent_primitives", {})
    return {"ok": True, "tool": "agent_primitives", "read_only": True, "payload": contract}


def tool_knowledge(args: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "tool": "tool_knowledge", "read_only": True, "payload": get_tool_knowledge()}


def tool_catalog(args: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "tool": "tool_catalog", "read_only": True, "payload": get_tool_catalog()}


def guardrails_contract(args: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "tool": "guardrails_contract", "read_only": True, "payload": get_guardrails()}


def public_api(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "tool": "public_api",
        "read_only": True,
        "payload": {
            "stable_surfaces": [
                "seed_system.core.bootstrap_context",
                "seed_system.core.architecture_contract",
                "seed_system.core.growth_model",
                "seed_system.core.tool_knowledge",
                "seed_system.core.tool_catalog",
                "seed_system.core.guardrails",
                "seed_system.core.validators",
                "seed_system.core.project_kb_mcp",
            ],
            "docs": ["docs/public-api.md", "docs/contracts/*.schema.json"],
        },
    }


def contract_validate(args: dict[str, Any]) -> dict[str, Any]:
    root = args.get("root") or ROOT
    return {"ok": True, "tool": "contract_validate", "read_only": True, "payload": validate_public_artifacts(root)}


TOOLS = [
    {"name": "kb_stats", "description": "Summarize markdown files under PROJECT_KB_ROOT.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kb_search", "description": "Search markdown files by keyword.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["query"]}},
    {"name": "architecture_contract", "description": "Return the canonical public architecture contract.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "maintenance_contract", "description": "Return the canonical maintenance contract.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "capability_index", "description": "Return the public capability index.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "agent_capabilities", "description": "Return the top-level agent capability list.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "growth_model", "description": "Return the reusable growth model.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "agent_primitives", "description": "Return the reusable agent primitive groups.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "tool_knowledge", "description": "Return reusable public tool and knowledge patterns.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "tool_catalog", "description": "Return the public MCP tool catalog.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "guardrails_contract", "description": "Return the public guardrails contract.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "public_api", "description": "Return the public API summary.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "contract_validate", "description": "Validate public seed-system artifacts.", "inputSchema": {"type": "object", "properties": {"root": {"type": "string"}}}},
    {"name": "bootstrap_context_pack", "description": "Generate a read-only agent bootstrap context pack.", "inputSchema": {"type": "object", "properties": {"workspace": {"type": "string"}, "project_id": {"type": "string"}, "task": {"type": "string"}, "depth": {"type": "string", "enum": ["quick", "normal", "deep"], "default": "normal"}, "json": {"type": "boolean", "default": False}}}},
]


def handle(req: dict[str, Any]) -> dict[str, Any] | None:
    method = req.get("method")
    req_id = req.get("id")
    if method == "initialize":
        version = (req.get("params") or {}).get("protocolVersion")
        if version not in SUPPORTED_PROTOCOL_VERSIONS:
            version = DEFAULT_PROTOCOL_VERSION
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": {"name": "seed-system", "version": "1.0.0"}}}
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        result = kb_stats() if name == "kb_stats" else kb_search(args) if name == "kb_search" else architecture_contract(args) if name == "architecture_contract" else maintenance_contract(args) if name == "maintenance_contract" else capability_index(args) if name == "capability_index" else agent_capabilities(args) if name == "agent_capabilities" else growth_model(args) if name == "growth_model" else agent_primitives(args) if name == "agent_primitives" else tool_knowledge(args) if name == "tool_knowledge" else tool_catalog(args) if name == "tool_catalog" else guardrails_contract(args) if name == "guardrails_contract" else public_api(args) if name == "public_api" else contract_validate(args) if name == "contract_validate" else bootstrap_context_pack(args) if name == "bootstrap_context_pack" else {"ok": False, "error": f"unknown tool: {name}"}
        return {"jsonrpc": "2.0", "id": req_id, "result": _text(result)}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"unknown method: {method}"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(json.dumps(handle(json.loads(line)), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
