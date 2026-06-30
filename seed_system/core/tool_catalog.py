"""Public tool catalog for seed-system MCP surfaces."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

TOOL_CATALOG_VERSION = "1.0.0"

TOOL_CATALOG: dict[str, Any] = {
    "version": TOOL_CATALOG_VERSION,
    "tools": [
        {"name": "kb_stats", "purpose": "Summarize markdown files.", "safety_level": "read-only", "read_only": True, "output_shape": "json object", "verification": "non-empty ok flag", "fallback": "manual file listing"},
        {"name": "kb_search", "purpose": "Search markdown knowledge files.", "safety_level": "read-only", "read_only": True, "output_shape": "matches list", "verification": "query required", "fallback": "text search"},
        {"name": "architecture_contract", "purpose": "Return architecture contract.", "safety_level": "read-only", "read_only": True, "output_shape": "contract object", "verification": "schema/version present", "fallback": "docs/architecture.md"},
        {"name": "maintenance_contract", "purpose": "Return maintenance contract.", "safety_level": "read-only", "read_only": True, "output_shape": "contract object", "verification": "snapshot/doctor/validate present", "fallback": "architecture contract"},
        {"name": "capability_index", "purpose": "Return public capability index.", "safety_level": "read-only", "read_only": True, "output_shape": "sections list", "verification": "sections present", "fallback": "architecture contract"},
        {"name": "agent_capabilities", "purpose": "Return top-level agent capabilities.", "safety_level": "read-only", "read_only": True, "output_shape": "capabilities list", "verification": "list present", "fallback": "capability index"},
        {"name": "growth_model", "purpose": "Return reusable growth loop.", "safety_level": "read-only", "read_only": True, "output_shape": "growth model object", "verification": "entrypoints present", "fallback": "docs/architecture.md"},
        {"name": "agent_primitives", "purpose": "Return reusable agent primitive groups.", "safety_level": "read-only", "read_only": True, "output_shape": "groups list", "verification": "groups present", "fallback": "growth model"},
        {"name": "tool_knowledge", "purpose": "Return reusable tool and knowledge patterns.", "safety_level": "read-only", "read_only": True, "output_shape": "tool groups and knowledge types", "verification": "tool_groups present", "fallback": "docs/architecture.md"},
        {"name": "tool_catalog", "purpose": "Return MCP tool catalog.", "safety_level": "read-only", "read_only": True, "output_shape": "tools list", "verification": "tool names present", "fallback": "project_kb_mcp.TOOLS"},
        {"name": "guardrails_contract", "purpose": "Return public safety guardrails.", "safety_level": "read-only", "read_only": True, "output_shape": "rules list", "verification": "rules present", "fallback": "docs/public-api.md"},
        {"name": "public_api", "purpose": "Return public API summary.", "safety_level": "read-only", "read_only": True, "output_shape": "stable surfaces and tools", "verification": "stable surfaces present", "fallback": "docs/public-api.md"},
        {"name": "contract_validate", "purpose": "Validate core public artifacts.", "safety_level": "read-only", "read_only": True, "output_shape": "validation report", "verification": "ok flag", "fallback": "manual schema review"},
        {"name": "bootstrap_context_pack", "purpose": "Generate a read-only bootstrap context pack.", "safety_level": "read-only", "read_only": True, "output_shape": "markdown or json payload", "verification": "bootstrap schema fields present", "fallback": "manual docs read"},
    ],
}


def get_tool_catalog() -> dict[str, Any]:
    return deepcopy(TOOL_CATALOG)

