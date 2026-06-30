"""Reusable public tool and knowledge patterns for generic agents."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

TOOL_KNOWLEDGE_VERSION = "1.0.0"

TOOL_KNOWLEDGE: dict[str, Any] = {
    "version": TOOL_KNOWLEDGE_VERSION,
    "purpose": "Expose reusable tool habits and knowledge patterns without private local configuration.",
    "tool_groups": [
        {
            "name": "code_navigation",
            "use_for": ["find symbols", "trace callers", "inspect blast radius", "read relevant files"],
            "principles": [
                "Prefer structural indexes when available.",
                "Use fast text search for broad discovery.",
                "Read the smallest set of files that explains the change.",
            ],
        },
        {
            "name": "safe_editing",
            "use_for": ["patch files", "preserve user changes", "keep edits scoped", "support rollback"],
            "principles": [
                "Back up before local mutation when policy requires it.",
                "Avoid unrelated refactors.",
                "Prefer patch-style edits for reviewable changes.",
            ],
        },
        {
            "name": "verification",
            "use_for": ["compile", "schema check", "smoke test", "compare examples", "validate contracts"],
            "principles": [
                "Verify the behavior touched by the change.",
                "Use quick checks first, full checks when risk is higher.",
                "Report unrun checks explicitly.",
            ],
        },
        {
            "name": "source_verification",
            "use_for": ["current facts", "libraries", "standards", "external systems", "recommendations"],
            "principles": [
                "Use primary sources for technical facts.",
                "Treat time-sensitive facts as unstable until checked.",
                "Keep citations or evidence links when using external sources.",
            ],
        },
        {
            "name": "tool_discovery",
            "use_for": ["find available MCP tools", "check tool health", "choose the smallest tool surface"],
            "principles": [
                "Discover tools before assuming they exist.",
                "Prefer read-only tool calls for inspection.",
                "Record unavailable tools as blockers or fallbacks.",
            ],
        },
        {
            "name": "browser_and_gui",
            "use_for": ["visual verification", "web app checks", "manual-entry surfaces", "screenshots"],
            "principles": [
                "Use HTTP checks when visual control is unavailable.",
                "Use browser automation for rendered UI evidence.",
                "Avoid brittle GUI automation when a direct API exists.",
            ],
        },
        {
            "name": "git_and_release",
            "use_for": ["status review", "diff review", "versioning", "release notes", "remote sync"],
            "principles": [
                "Inspect working tree status before summarizing changes.",
                "Keep release notes user-facing.",
                "Do not commit backups or generated caches.",
            ],
        },
        {
            "name": "memory_and_skills",
            "use_for": ["retain reusable lessons", "author skills", "align drifted skills", "avoid context-only rules"],
            "principles": [
                "Promote durable lessons into explicit files.",
                "Keep skills auditable and scoped.",
                "Do not rely on chat context for system rules.",
            ],
        },
    ],
    "knowledge_types": [
        {
            "name": "stable_contract",
            "examples": ["schemas", "public APIs", "architecture contracts", "skill templates"],
            "handling": "Can be reused after checking local version compatibility.",
        },
        {
            "name": "live_state",
            "examples": ["running services", "ports", "tool availability", "current permissions"],
            "handling": "Must be verified in the current environment.",
        },
        {
            "name": "private_runtime",
            "examples": ["tokens", "local logs", "user-specific paths", "account data"],
            "handling": "Do not publish; sanitize or keep local-only.",
        },
        {
            "name": "reusable_lesson",
            "examples": ["failure modes", "repair patterns", "validation rules", "workflow conventions"],
            "handling": "Promote into docs, skills, examples, or contracts when broadly useful.",
        },
    ],
}


def get_tool_knowledge() -> dict[str, Any]:
    return deepcopy(TOOL_KNOWLEDGE)

